import datetime
from . import models, db


def create_user(username, password, admin, active):
    user = models.User(username=username, password=password, admin=admin, active=active)
    db.session.add(user)
    db.session.commit()
    return user


def create_task(created_by, planned_at, assigned_to_id, origin, destination, comments, estimated_price, time_to_arrive, status=models.TaskStatus.NEW):
    if planned_at is None:
        planned_at = datetime.datetime.utcnow()
    print('estimated_price: {}, time_to_arrive: {}'.format(estimated_price, time_to_arrive))
    task = models.Task(
        created_by=created_by,
        planned_at=planned_at,
        assigned_to_id=assigned_to_id,
        origin=origin,
        destination=destination,
        status=status,
        comments=comments,
        parent_task_id=None,
        estimated_price=estimated_price,
        time_to_arrive=time_to_arrive
    )
    db.session.add(task)
    db.session.commit()
    return task


def _copy_task(task):
    return models.Task(
        created_by=task.created_by,
        planned_at=task.planned_at,
        assigned_to=task.assigned_to,
        origin=task.origin,
        destination=task.destination,
        status=task.status,
        parent_task_id=task.id,
        estimated_price=task.estimated_price,
        time_to_arrive=task.time_to_arrive
    )


def update_task(task_id, created_by, planned_at, assigned_to_id, origin, destination, comments, estimated_price, real_price, time_to_arrive, status):
    task = models.Task.query.get(task_id)
    task_history = _copy_task(task)

    task.created_by = created_by
    task.planned_at = planned_at
    task.assigned_to_id = assigned_to_id
    task.origin = origin
    task.destination = destination
    task.comments = comments
    task.estimated_price = estimated_price
    task.real_price = real_price
    task.time_to_arrive = time_to_arrive
    task.status = status

    db.session.add(task_history)
    db.session.commit()


def update_task_status(user, task_id, status, **kwargs):
    #TODO lock for update
    task = models.Task.query.get(task_id)
    #TODO check rights
    task_history = _copy_task(task)

    if status == models.TaskStatus.NEW:
        pass
    elif status == models.TaskStatus.CLAIMED:
        task.status = models.TaskStatus.CLAIMED
        task.assigned_to_id = user.id
    elif status == models.TaskStatus.PROCESSING:
        task.status = models.TaskStatus.PROCESSING
    elif status == models.TaskStatus.FINISHED:
        task.status = models.TaskStatus.FINISHED
        if 'price' in kwargs:
            task.real_price = kwargs['price']
    else:
        pass

    # if 'comment' in kwargs:
    #     c = task.comments + '\n' if task.comments else ''
    #     task.comments = c + kwargs['comment']

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
    c = task.comments + '\n' if task.comments else ''
    task.comments = c + comment
    db.session.add(task_history)
    db.session.commit()


def find_active_tasks_for_user(user):
    if user.is_admin():
        return models.Task.query.filter(models.Task.parent_task==None, models.Task.archived==False)
    else:
        return models.Task.query.filter(models.Task.parent_task==None, models.Task.assigned_to_id==user.id, models.Task.archived==False)


def find_all_tasks():
    return models.Task.query.filter(models.Task.parent_task==None)


def get_task(id, user):
    return models.Task.query.get(id)


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


def find_unseen_messages():
    return models.Message.query.filter(models.Message.seen==False)


def update_messages_as_seen():
    models.Message.query.update({models.Message.seen: True})
    db.session.commit()


def create_message(created_by, task_id, message):
    message = models.Message(created_by=created_by, task_id=task_id, message=message)
    db.session.add(message)
    db.session.commit()
    return message
