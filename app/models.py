import binascii
import os
import enum
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, backref
from . import db, login_manager, app
from .utils import current_datetime
from datetime import timedelta
from flask_babel import lazy_gettext as _


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    hashed_password = db.Column(db.String(160))
    admin = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    last_seen = db.Column(db.DateTime(), default=current_datetime)

    def __init__(self, username, password="changeme123", admin=False, active=True):
        self.username = username
        self.set_password(password)
        self.admin = admin
        self.active = active
        self.is_authenticated = False

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return self.is_authenticated

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.admin

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def to_json(self, user):
        return {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.strftime(app.config['DATETIME_FORMAT']) if self.last_seen is not None else None,
        }


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class TaskStatus(enum.Enum):
    NEW = _('TaskStatus.NEW')
    CLAIMED = _('TaskStatus.CLAIMED')
    PROCESSING = _('TaskStatus.PROCESSING')
    FINISHED = _('TaskStatus.FINISHED')
    CANCELLED = _('TaskStatus.CANCELLED')


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=current_datetime)
    updated_at = db.Column(db.DateTime, default=current_datetime, onupdate=current_datetime)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = relationship(User, foreign_keys=(created_by_id,))
    planned_at = db.Column(db.DateTime, default=current_datetime)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_to = relationship(User, foreign_keys=(assigned_to_id,))
    origin = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    comments = db.Column(db.Text)
    status = db.Column(db.Enum(TaskStatus))
    archived = db.Column(db.Boolean, default=False)
    real_price = db.Column(db.Numeric(6, 2))
    estimated_price = db.Column(db.Numeric(6, 2))
    time_to_arrive = db.Column(db.Integer, default=0)
    parent_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    parent_task = relationship('Task', remote_side=id)
    history = relationship('Task', backref=backref('parent', remote_side=[id], order_by='desc(Task.created_at)'))

    '''
    @property
    def timestamp_fmt(self):
        return self.timestamp.strftime('%Y-%m-%dT%H:%M:%S Z')
    '''

    @property
    def time_to_arrive_calculated(self):
        planned = self.planned_at if self.planned_at is not None else self.created_at
        td = planned.timestamp() - current_datetime().timestamp() + timedelta(minutes=self.time_to_arrive).total_seconds()
        return td // 60

    def __repr__(self):
        return '<Task {0} {1} {2} {3} {4} {5} {6}>'.format(self.id, self.created_at, self.updated_at, self.status, self.archived, self.parent_task_id, self.history)

    def from_json(self, data):
        # TODO: implement
        pass

    def to_json(self, user):
        return {
            'id': self.id,
            'created_at': self.created_at.strftime(app.config['DATETIME_FORMAT']),
            'created_by': self.created_by.username,
            'planned_at': self.planned_at.strftime(app.config['DATETIME_FORMAT']) if self.planned_at is not None else None,
            'assigned_to': self.assigned_to.username if self.assigned_to is not None else None,
            'assigned_to_id': self.assigned_to_id,
            'origin': self.origin,
            'destination': self.destination,
            'comments': self.comments,
            'status': self.status.name,
            'status_localized': self.status.value,
            'archived': self.archived,
            'real_price': str(self.real_price) if self.real_price is not None else None,
            'estimated_price': str(self.estimated_price) if self.estimated_price is not None else None,
            'time_to_arrive': self.time_to_arrive,
            'time_to_arrive_calculated': self.time_to_arrive_calculated,
            'available_actions': ','.join(self.available_actions(user))
        }

    def available_actions(self, user):
        actions = list()
        if user.is_admin():
            actions.append('can_edit')
        else:
            if self.can_claim(user):
                actions.append('can_claim')
            if self.can_start_progress(user):
                actions.append('can_start_progress')
            if self.can_request_call_customer(user):
                actions.append('can_request_call_customer')
            if self.can_request_call_me(user):
                actions.append('can_request_call_me')
            if self.can_change_route(user):
                actions.append('can_change_route')
            if self.can_finish_task(user):
                actions.append('can_finish_task')

        return actions

    def can_claim(self, user):
        return (self.assigned_to is None or self.assigned_to == user) and self.status == TaskStatus.NEW

    def can_start_progress(self, user):
        return self.assigned_to == user and self.status == TaskStatus.CLAIMED

    def can_request_call_customer(self, user):
        return self.assigned_to == user and self.status == TaskStatus.CLAIMED

    def can_request_call_me(self, user):
        return self.assigned_to == user and self.status == TaskStatus.CLAIMED

    def can_change_route(self, user):
        return self.assigned_to == user and self.status == TaskStatus.CLAIMED

    def can_finish_task(self, user):
        return (self.assigned_to == user and self.status == TaskStatus.PROCESSING)

    def can_edit_task(self, user):
        return user.is_admin()


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=current_datetime)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = relationship(User, foreign_keys=(created_by_id,))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    message = db.Column(db.String(100))
    seen = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'created_by': self.created_by.username,
            'task_id': self.task_id,
            'message': self.message,
            'seen': self.seen
        }


class Shift(db.Model):
    __tablename__ = 'shifts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship(User, foreign_keys=(user_id,))
    started_at = db.Column(db.DateTime, default=current_datetime)

    def to_json(self):
        return {
            'id': self.id,
            'started_at': self.started_at,
            'user': self.user.username
        }
