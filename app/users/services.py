from app.models import User, load_user
from app import db
from app.utils import current_datetime


def find_user_by_id(user_id):
    return User.query.get(user_id)


def find_active_users():
    return User.query.filter(User.active==True)


def create_user(username, password, admin, active):
    user = User(username=username, password=password, admin=admin, active=active)
    db.session.add(user)
    db.session.commit()
    return user


def is_user_admin(user_id):
    user = load_user(user_id)
    return user.is_admin() if user is not None else None


def valid_login(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return None
    if user.check_password(password):
        return user
    else:
        return None


def ping(user):
    user.last_seen = current_datetime()
    db.session.add(user)
    db.session.commit()
