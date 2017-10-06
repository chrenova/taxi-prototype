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

    t1 = services.create_task(created_by=u1, assigned_to=u2, origin='ba', destination='nr', status=models.TaskStatus.NEW, comments='short comment')
    services.create_task(created_by=u2, assigned_to=u3, origin='nr', destination='bb', status=models.TaskStatus.PROCESSING, comments='')
    services.create_task(created_by=u3, assigned_to=u1, origin='ke', destination='po', status=models.TaskStatus.FINISHED, comments='short comment')
    services.create_task(created_by=u1, assigned_to=u2, origin='ba', destination='nr', status=models.TaskStatus.NEW, comments='')
    services.create_task(created_by=u2, assigned_to=u3, origin='nr', destination='bb', status=models.TaskStatus.PROCESSING, comments='short comment')
    services.create_task(created_by=u3, assigned_to=u1, origin='ke', destination='po', status=models.TaskStatus.FINISHED, comments='')
    services.create_task(created_by=u1, assigned_to=u2, origin='ba', destination='nr', status=models.TaskStatus.NEW, comments='short comment')
    services.create_task(created_by=u1, assigned_to=u2, origin='po', destination='zv', status=models.TaskStatus.NEW, comments='short comment')
    services.create_task(created_by=u1, assigned_to=u2, origin='rk', destination='bb', status=models.TaskStatus.NEW, comments='short comment')
    services.create_task(created_by=u1, assigned_to=u2, origin='nz', destination='vt', status=models.TaskStatus.NEW, comments='short comment')
    services.create_task(created_by=u1, assigned_to=u2, origin='no', destination='ke', status=models.TaskStatus.NEW, comments='short comment')


    services.update_task_status(u1, t1.id, models.TaskStatus.PROCESSING)
    services.update_task_status(u1, t1.id, models.TaskStatus.FINISHED)
    services.update_task_set_archived(u1, t1.id)

    for t in services.find_all_tasks():
        print(t)


if __name__ == '__main__':
    main()
