import datetime
from app import db
from app.models import Task, TaskStatus, User
from app.tasks import services as task_services


def main():
    db.drop_all()
    db.create_all()

    u1 = User(username='qwerty', password='qwerty', admin=True, active=True)
    u2 = User(username='asdfgh', password='asdfgh', admin=False, active=True)
    u3 = User(username='zxcvbn', password='zxcvbn', admin=False, active=True)
    u4 = User(username='inactive', password='inactive', admin=False, active=False)
    db.session.add_all([u1, u2, u3, u4])
    db.session.commit()

    planned_tomorrow = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    t1 = task_services.create_task(created_by=u1, planned_at=None, assigned_to_id=u2.id, origin='ba', destination='nr', status=TaskStatus.NEW, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    task_services.create_task(created_by=u2, planned_at=None, assigned_to_id=u3.id, origin='nr', destination='', status=TaskStatus.PROCESSING, comments='', estimated_price=2.5, time_to_arrive=15)
    task_services.create_task(created_by=u3, planned_at=planned_tomorrow, assigned_to_id=u1.id, origin='ke', destination='po', status=TaskStatus.FINISHED, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    task_services.create_task(created_by=u1, planned_at=None, assigned_to_id=None, origin='ba', destination='nr', status=TaskStatus.NEW, comments='', estimated_price=5.5, time_to_arrive=10)
    task_services.create_task(created_by=u2, planned_at=planned_tomorrow, assigned_to_id=u3.id, origin='nr', destination='bb', status=TaskStatus.PROCESSING, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    task_services.create_task(created_by=u3, planned_at=None, assigned_to_id=u1.id, origin='ke', destination='po', status=TaskStatus.FINISHED, comments='', estimated_price=5.5, time_to_arrive=10)
    task_services.create_task(created_by=u1, planned_at=planned_tomorrow, assigned_to_id=u2.id, origin='ba', destination='nr', status=TaskStatus.NEW, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    task_services.create_task(created_by=u1, planned_at=None, assigned_to_id=u2.id, origin='po', destination='zv', status=TaskStatus.CLAIMED, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    task_services.create_task(created_by=u1, planned_at=None, assigned_to_id=u2.id, origin='rk', destination='bb', status=TaskStatus.NEW, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    task_services.create_task(created_by=u1, planned_at=planned_tomorrow, assigned_to_id=u2.id, origin='nz', destination='vt', status=TaskStatus.CLAIMED, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    task_services.create_task(created_by=u1, planned_at=None, assigned_to_id=u2.id, origin='no', destination='ke', status=TaskStatus.PROCESSING, comments='short comment', estimated_price=5.5, time_to_arrive=10)

    task_services.update_task_status(u1, t1.id, TaskStatus.PROCESSING)
    task_services.update_task_status(u1, t1.id, TaskStatus.FINISHED)
    task_services.update_task_set_archived(u1, t1.id)

    for t in task_services.find_all_tasks():
        print(t)


if __name__ == '__main__':
    main()
