from app import db, models


def main():
    for u in db.session.query(models.User).all():
        print(u)
    for t in db.session.query(models.Task).all():
        print(t)


if __name__ == '__main__':
    main()
