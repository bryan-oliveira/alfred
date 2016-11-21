from app.models import Allergy, Users
from app import db
import sys


def insert_user(user, allergies):
    print >> sys.stderr, user, allergies

    if not isinstance(user, Users) and not isinstance(allergies, Allergy):
        return False, '[Insert User] Invalid user info.'

    # Insert a Person in the users table
    new_person = Users(fullname=user.fullname, username=user.username, age=user.age,
                       gender=user.gender, password=user.password)
    """
    new_person.allergies = Allergy(soy=allergies.soy, milk=allergies.milk, eggs=allergies.eggs,
                                   nuts=allergies.nuts, gluten=allergies.gluten, fish=allergies.fish,
                                   sesame=allergies.sesame)
    """

    print >> sys.stderr, 'USER:', user.fullname, user.age, user.gender, user.password, user.username

    print >> sys.stderr, 'Obj > Name:', new_person.fullname, 'User:', new_person.username, 'Age:', new_person.age, \
        'Gender:', new_person.gender, 'Pass:', new_person.password

    """
     print 'Milk:', new_person.allergies.milk, 'Soy:', new_person.allergies.soy, \
        'Gluten:', new_person.allergies.gluten, 'Fish:', new_person.allergies.fish, \
        'Sesame:', new_person.allergies.sesame, 'Nuts:', new_person.allergies.nuts, \
        'Eggs:', new_person.allergies.eggs
    """

    print >> sys.stderr, "Adding user to db."
    db.session.add(new_person)
    print >> sys.stderr, "Added !"
    print >> sys.stderr, "Commiting..."
    db.session.commit()

    print >> sys.stderr, 'User added!'
    return True, ''

if __name__ == '__main__':
    u1 = Users(fullname='Bryan Oliveira', username='bryan', age=30, gender='M', password='1234')
    a1 = Allergy(soy=True, milk=False, eggs=False, nuts=False, gluten=False, fish=False, sesame=False, )

    u2 = Users(fullname='Zyanya Garrido', username='bebito', age=26, gender='F', password='1234')
    a2 = Allergy(soy=False, milk=False, eggs=False, nuts=False, gluten=False, fish=False, sesame=True)

    u3 = Users(fullname='Francisco Mendes', username='balao', age=29, gender='M', password='1234')
    a3 = Allergy(soy=False, milk=False, eggs=True, nuts=False, gluten=True, fish=False, sesame=False)

    insert_user(u1, a1)
    insert_user(u2, a2)
    insert_user(u3, a3)

