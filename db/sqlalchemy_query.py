from alfred_db import Users
from sqlalchemy_init import get_session
from sqlalchemy import and_


# Make a query to find all Persons in the database
def query_all_users():
    sess = get_session()
    print "Users:", sess.query(Users).count()
    users = sess.query(Users).all()

    for person in users:
        # Return the first Person from all Persons in the database
        print "Full Name:", person.fullname, "Password:", person.password, "Username:", person.username, \
            "Age:", person.age, "Gender:", person.gender, "ID:", person.id

        print "Allergies - User ID:", person.allergies.user_id, "Milk:", person.allergies.milk, \
            "Eggs:", person.allergies.eggs, "Nuts:", person.allergies.nuts, \
            "Gluten:", person.allergies.gluten, "Fish:", person.allergies.fish, \
            "Sesame:", person.allergies.sesame


def is_username_free(username):
    sess1 = get_session()
    users = sess1.query(Users).all()

    for person in users:
        if person.username == username:
            return False
    return True


def check_credentials(user, pwd):
    sess = get_session()
    res = sess.query(Users).filter(and_(Users.username == user, Users.password == pwd)).all()

    if len(res) > 0:
        print res[0].fullname
        return True, ''
    return False, 'Invalid Username / Password. Please try again'

if __name__ == '__main__':
    query_all_users()
