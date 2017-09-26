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

    t1 = services.create_task(created_by=u1, assigned_to=u2, origin='ba', destination='nr', status=models.TaskStatus.NEW)
    t2 = services.create_task(created_by=u2, assigned_to=u3, origin='nr', destination='bb', status=models.TaskStatus.PROCESSING)
    t3 = services.create_task(created_by=u3, assigned_to=u1, origin='ke', destination='po', status=models.TaskStatus.FINISHED)
    t4 = services.create_task(created_by=u1, assigned_to=u2, origin='ba', destination='nr', status=models.TaskStatus.NEW)
    t5 = services.create_task(created_by=u2, assigned_to=u3, origin='nr', destination='bb', status=models.TaskStatus.PROCESSING)
    t6 = services.create_task(created_by=u3, assigned_to=u1, origin='ke', destination='po', status=models.TaskStatus.FINISHED)

    services.update_task_set_processing(u1, t1.id)
    services.update_task_set_finished(u1, t1.id)
    services.update_task_set_archived(u1, t1.id)

    for t in services.find_all_tasks():
        print(t)


if __name__ == '__main__':
    main()
