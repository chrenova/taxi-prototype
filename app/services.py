import datetime
from . import models, db


def create_task(created_by, assigned_to, origin, destination, comments, status=models.TaskStatus.NEW):
    task = models.Task(created_by=created_by, assigned_to=assigned_to, origin=origin, destination=destination, status=status, comments=comments, parent_task_id=None)
    db.session.add(task)
    db.session.commit()
    return task


def _copy_task(task):
    return models.Task(created_by=task.created_by, assigned_to=task.assigned_to, origin=task.origin, destination=task.destination, status=task.status, parent_task_id=task.id)


def update_task(task_id):
    task = models.Task.query.get(task_id)
    task_history = _copy_task(task)
    db.session.add(task_history)
    db.session.commit()


def update_task_set_processing(user, task_id):
    #TODO lock for update
    task = models.Task.query.get(task_id)
    #TODO check rights
    task_history = _copy_task(task)
    task.status = models.TaskStatus.PROCESSING
    task.assigned_to_id = user.id
    db.session.add(task_history)
    db.session.commit()


def update_task_set_finished(user, task_id):
    #TODO lock for update
    task = models.Task.query.get(task_id)
    #TODO check rights
    task_history = _copy_task(task)
    task.status = models.TaskStatus.FINISHED
    db.session.add(task_history)
    db.session.commit()


def update_task_set_archived(user, task_id):
    #TODO lock for update
    task = models.Task.query.get(task_id)
    #TODO check rights
    task_history = _copy_task(task)
    task.archived = True
    db.session.add(task_history)
    db.session.commit()


def update_task_add_comment(user, task_id, comment):
    # TODO lock for update
    task = models.Task.query.get(task_id)
    #TODO check rights
    task_history = _copy_task(task)
    task.comments = (task.comments + '\n' if task.comments is not None else '') + comment
    db.session.add(task_history)
    db.session.commit()


def find_active_tasks_for_user(user):
    return models.Task.query.filter(models.Task.parent_task==None, models.Task.assigned_to_id==user.id)


def find_all_tasks():
    return models.Task.query.filter(models.Task.parent_task==None)


def is_user_admin(user_id):
    user = models.load_user(user_id)
    return user.is_admin() if user is not None else None


def valid_login(username, password):
    user = models.User.query.filter_by(username=username).first()
    if user is None:
        return None
    if user.check_password(password):
        return user
    else:
        return None

def find_user_by_id(user_id):
    return models.User.query.get(user_id)

def find_active_users():
    return models.User.query.filter(models.User.active==True)
