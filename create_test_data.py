import datetime
from app import db, models, services


def main():
    db.drop_all()
    db.create_all()

    u1 = models.User(username='qwerty', password='qwerty', admin=True, active=True)
    u2 = models.User(username='asdfgh', password='asdfgh', admin=False, active=True)
    u3 = models.User(username='zxcvbn', password='zxcvbn', admin=False, active=True)
    u4 = models.User(username='inactive', password='inactive', admin=False, active=False)
    db.session.add_all([u1, u2, u3, u4])
    db.session.commit()

    planned_tomorrow = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    t1 = services.create_task(created_by=u1, planned_at=None, assigned_to_id=u2.id, origin='ba', destination='nr', status=models.TaskStatus.NEW, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    services.create_task(created_by=u2, planned_at=None, assigned_to_id=u3.id, origin='nr', destination='', status=models.TaskStatus.PROCESSING, comments='', estimated_price=2.5, time_to_arrive=15)
    services.create_task(created_by=u3, planned_at=planned_tomorrow, assigned_to_id=u1.id, origin='ke', destination='po', status=models.TaskStatus.FINISHED, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    services.create_task(created_by=u1, planned_at=None, assigned_to_id=None, origin='ba', destination='nr', status=models.TaskStatus.NEW, comments='', estimated_price=5.5, time_to_arrive=10)
    services.create_task(created_by=u2, planned_at=planned_tomorrow, assigned_to_id=u3.id, origin='nr', destination='bb', status=models.TaskStatus.PROCESSING, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    services.create_task(created_by=u3, planned_at=None, assigned_to_id=u1.id, origin='ke', destination='po', status=models.TaskStatus.FINISHED, comments='', estimated_price=5.5, time_to_arrive=10)
    services.create_task(created_by=u1, planned_at=planned_tomorrow, assigned_to_id=u2.id, origin='ba', destination='nr', status=models.TaskStatus.NEW, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    services.create_task(created_by=u1, planned_at=None, assigned_to_id=u2.id, origin='po', destination='zv', status=models.TaskStatus.CLAIMED, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    services.create_task(created_by=u1, planned_at=None, assigned_to_id=u2.id, origin='rk', destination='bb', status=models.TaskStatus.NEW, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    services.create_task(created_by=u1, planned_at=planned_tomorrow, assigned_to_id=u2.id, origin='nz', destination='vt', status=models.TaskStatus.CLAIMED, comments='short comment', estimated_price=5.5, time_to_arrive=10)
    services.create_task(created_by=u1, planned_at=None, assigned_to_id=u2.id, origin='no', destination='ke', status=models.TaskStatus.PROCESSING, comments='short comment', estimated_price=5.5, time_to_arrive=10)

    services.update_task_status(u1, t1.id, models.TaskStatus.PROCESSING)
    services.update_task_status(u1, t1.id, models.TaskStatus.FINISHED)
    services.update_task_set_archived(u1, t1.id)

    for t in services.find_all_tasks():
        print(t)


if __name__ == '__main__':
    main()
