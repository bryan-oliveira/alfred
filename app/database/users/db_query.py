# from alfred_db import Users
# from sqlalchemy_init import get_session
# from sqlalchemy import and_
from app import models


# Make a query to find all Persons in the database
def query_all_users():

    users = models.Users.query.all()

    for person in users:
        # Return the first Person from all Persons in the database

        """
        print "Allergies - User ID:", person.allergies.user_id, "Milk:", person.allergies.milk, \
            "Eggs:", person.allergies.eggs, "Nuts:", person.allergies.nuts, \
            "Gluten:", person.allergies.gluten, "Fish:", person.allergies.fish, \
            "Sesame:", person.allergies.sesame
        """


def is_username_free(username):

    users = models.Users.query.all()

    for person in users:
        if person.username == username:
            return False
    return True


if __name__ == '__main__':
    query_all_users()
