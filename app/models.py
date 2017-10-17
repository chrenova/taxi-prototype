import binascii
import os
import enum
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, backref
from . import db, login_manager
from datetime import datetime
from flask_babel import lazy_gettext as _


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    hashed_password = db.Column(db.String(160))
    admin = db.Column(db.Boolean)
    active = db.Column(db.Boolean)

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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class TaskStatus(enum.Enum):
    NEW = _('TaskStatus.NEW')
    PROCESSING = _('TaskStatus.PROCESSING')
    FINISHED = _('TaskStatus.FINISHED')


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = relationship(User, foreign_keys=(created_by_id,))
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_to = relationship(User, foreign_keys=(assigned_to_id,))
    origin = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    comments = db.Column(db.Text)
    status = db.Column(db.Enum(TaskStatus))
    archived = db.Column(db.Boolean, default=False)
    value = db.Column(db.Numeric(6, 2))
    parent_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    parent_task = relationship('Task', remote_side=id)
    history = relationship('Task', backref=backref('parent', remote_side=[id], order_by='desc(Task.created_at)'))

    '''
    @property
    def timestamp_fmt(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    '''

    def __repr__(self):
        return '<Task {0} {1} {2} {3} {4} {5} {6}>'.format(self.id, self.created_at, self.updated_at, self.status, self.archived, self.parent_task_id, self.history)

    def to_json(self, user):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'created_by': self.created_by.username,
            'assigned_to': self.assigned_to.username,
            'origin': self.origin,
            'destination': self.destination,
            'comments': self.comments,
            'status': self.status.name,
            'status_localized': self.status.value,
            'archived': self.archived,
            'value': str(self.value) if self.value is not None else None,
            'can_start_progress': self.can_start_progress(user),
            'can_add_comment': self.can_add_comment(user),
            'can_finish_task': self.can_finish_task(user),
            'can_archive_task': self.can_archive_task(user),
            'can_edit_task': self.can_edit_task(user)
        }

    def can_start_progress(self, user):
        return (self.assigned_to is None or self.assigned_to == user) and self.status == TaskStatus.NEW

    def can_add_comment(self, user):
        return (self.assigned_to is None or self.assigned_to == user) or user.is_admin()

    def can_finish_task(self, user):
        return (self.assigned_to == user and self.status == TaskStatus.PROCESSING) or user.is_admin()

    def can_archive_task(self, user):
        return self.status == TaskStatus.FINISHED and user.is_admin()

    def can_edit_task(self, user):
        return user.is_admin()
