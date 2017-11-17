import datetime
from app.models import Task, TaskStatus
from app import db


def create_task(created_by, planned_at, assigned_to_id, origin, destination, comments, estimated_price, time_to_arrive, status=TaskStatus.NEW):
    if planned_at is None:
        planned_at = datetime.datetime.utcnow()
    print('estimated_price: {}, time_to_arrive: {}'.format(estimated_price, time_to_arrive))
    task = Task(
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
    return Task(
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
    task = Task.query.get(task_id)
    task_history = _copy_task(task)

    task.created_by = created_by
    print('planned_at: {}'.format(planned_at))
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
    task = Task.query.get(task_id)
    #TODO check rights
    task_history = _copy_task(task)

    if status == TaskStatus.NEW:
        pass
    elif status == TaskStatus.CLAIMED:
        task.status = TaskStatus.CLAIMED
        task.assigned_to_id = user.id
    elif status == TaskStatus.PROCESSING:
        task.status = TaskStatus.PROCESSING
    elif status == TaskStatus.FINISHED:
        task.status = TaskStatus.FINISHED
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
    task = Task.query.get(task_id)
    #TODO check rights
    task_history = _copy_task(task)
    task.archived = True
    db.session.add(task_history)
    db.session.commit()


def update_task_add_comment(user, task_id, comment):
    # TODO lock for update
    task = Task.query.get(task_id)
    #TODO check rights
    task_history = _copy_task(task)
    c = task.comments + '\n' if task.comments else ''
    task.comments = c + comment
    db.session.add(task_history)
    db.session.commit()


def find_active_tasks_for_user(user):
    if user.is_admin():
        return Task.query.filter(Task.parent_task==None, Task.archived==False)
    else:
        return Task.query.filter(Task.parent_task==None, Task.assigned_to_id==user.id, Task.archived==False)


def find_future_tasks_for_user(user):
    if user.is_admin():
        return Task.query.filter(Task.parent_task==None, Task.archived==False)
    else:
        return Task.query.filter(Task.parent_task==None, Task.assigned_to_id==user.id, Task.archived==False)


def find_all_tasks():
    return Task.query.filter(Task.parent_task==None)


def get_task(id, user):
    return Task.query.get(id)
