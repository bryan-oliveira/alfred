from app.models import Allergy, User
from app import db
from datetime import datetime
from app import bcrypt


def create_admin():
    u = User(
        fullname="Bryan Oliveira",
        username="bryan",
        email="vicdaruf@yahoo.com",
        password="123123",
        age=100,
        gender="M",
        confirmed=True,
        admin=True)

    a = Allergy()
    u.allergy = a

    db.session.add(u)
    db.session.commit()


def insert_user(user, allergies):

    if not isinstance(user, User) and not isinstance(allergies, Allergy):
        return False, 'Error inserting user. Invalid user info.'

    # Insert a Person in the users table
    user.allergy = allergies

    db.session.add(user)
    db.session.commit()

    return True, ''


def edit_user(user, form, update_pwd):
    edit = False

    if user.fullname != form.fullname.data:
        user.fullname = form.fullname.data
        edit = True

    if user.username != form.username.data:
        user.username = form.username.data
        edit = True

    if user.email != form.email.data:
        user.email = form.email.data
        edit = True

    if user.age != form.age.data:
        user.age = form.age.data
        edit = True

    if user.gender != form.gender.data:
        user.gender = form.gender.data
        edit = True

    # TODO_ Password

    if user.allergy.lowchol != form.lowchol.data:
        user.allergy.lowchol = form.lowchol.data
        edit = True

    if user.allergy.highchol != form.highchol.data:
        user.allergy.highchol = form.highchol.data
        edit = True

    if user.allergy.underw != form.underw.data:
        user.allergy.underw = form.underw.data
        edit = True

    if user.allergy.overw != form.overw.data:
        user.allergy.overw = form.overw.data
        edit = True

    if user.allergy.gluten != form.gluten.data:
        user.allergy.gluten = form.gluten.data
        edit = True

    if user.allergy.nuts != form.nuts.data:
        user.allergy.nuts = form.nuts.data
        edit = True

    if user.allergy.sesame != form.sesame.data:
        user.allergy.sesame = form.sesame.data
        edit = True

    if user.allergy.vegetarian != form.vegetarian.data:
        user.allergy.vegetarian = form.vegetarian.data
        edit = True

    if user.allergy.vegan != form.vegan.data:
        user.allergy.vegan = form.vegan.data
        edit = True

    # If password field is not empty, update user password hash
    if update_pwd:
        user.password = bcrypt.generate_password_hash(form.new_password.data)
        edit = True

    if edit == True:
        db.session.commit()
        return True

    return False


if __name__ == '__main__':
    create_admin()

