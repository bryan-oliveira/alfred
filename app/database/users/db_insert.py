from app.models import Allergy, Users
from app import db

def insert_user(user, allergies):
    # [#] print sys.stderr, user, allergies

    if not isinstance(user, Users) and not isinstance(allergies, Allergy):
        return False, 'Error inserting user. Invalid user info.'

    # Insert a Person in the users table
    user.allergy = allergies

    db.session.add(user)
    db.session.commit()

    return True, ''

if __name__ == '__main__':
    u1 = Users(fullname='Bryan Oliveira', username='bryan', age=30, gender='M', password='123123')
    a1 = Allergy(soy=True, milk=False, eggs=False, nuts=False, gluten=False, fish=False, sesame=False, )

    u2 = Users(fullname='Zyanya Garrido', username='bebito', age=26, gender='F', password='123123')
    a2 = Allergy(soy=False, milk=False, eggs=False, nuts=False, gluten=False, fish=False, sesame=True)

    u3 = Users(fullname='Francisco Mendes', username='balao', age=29, gender='M', password='123123')
    a3 = Allergy(soy=False, milk=False, eggs=True, nuts=False, gluten=True, fish=False, sesame=False)

    insert_user(u1, a1)
    insert_user(u2, a2)
    insert_user(u3, a3)

