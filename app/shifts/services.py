from app.models import Shift
from app import db


def start_new_shift(user):
    shift = Shift(user=user)
    db.session.add(shift)
    db.session.commit()
    return shift


def find_shifts_for_user(user):
    # TODO user may be empty
    # admin vs non-admin
    return Shift.query.filter(user=user)
