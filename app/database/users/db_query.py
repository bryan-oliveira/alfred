# from alfred_db import Users
# from sqlalchemy_init import get_session
# from sqlalchemy import and_
from app import models


def get_user_by_id(id_):
    user = models.Users.query.get(id_)
    allergy = models.Allergy.query.get(user.id)
    return user, allergy


def is_username_free(username):

    users = models.Users.query.all()

    for person in users:
        if person.username == username:
            return False
    return True


def list_all_users():
    users = models.Users.query.all()
    for user in users:
        print user, user.password

if __name__ == '__main__':
    list_all_users()

