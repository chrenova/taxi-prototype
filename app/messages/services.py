from app.models import Message
from app import db


def find_unseen_messages():
    return Message.query.filter(Message.seen==False)


def update_messages_as_seen():
    Message.query.update({Message.seen: True})
    db.session.commit()


def create_message(created_by, task_id, message):
    message = Message(created_by=created_by, task_id=task_id, message=message)
    db.session.add(message)
    db.session.commit()
    return message
