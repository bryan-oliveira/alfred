from app.database.users.db_query import is_username_free, email_is_free
from app.database.users.db_insert import insert_user
from app.models import User, Allergy


def register_account(form):
    # User information
    fullname = form['fullname'].data
    username = form['username'].data.lower()
    email = form['email'].data.lower()
    password = form['password'].data
    age = form['age'].data
    gender = form['gender'].data

    # Allergies/Restrictions
    lowchol = form.lowchol.data
    highchol = form.highchol.data
    overw = form.overw.data
    underw = form.underw.data
    nuts = form.nuts.data
    fish = form.fish.data
    sesame = form.sesame.data
    gluten = form.gluten.data
    vegetarian = form.vegetarian.data
    vegan = form.vegan.data

    if not email_is_free(email):
        return False, 'Email is already registered with another account.'

    if password != form.password_conf.data:
        return False, 'Passwords dont match. Please verify.'

    u1 = User(
        fullname=fullname,
        username=username,
        email=email,
        password=password,
        age=age,
        gender=gender,
        confirmed=False,
        admin=False)

    a1 = Allergy(lowchol=lowchol, highchol=highchol, overw=overw, underw=underw, nuts=nuts,
                 gluten=gluten, fish=fish, sesame=sesame, vegetarian=vegetarian, vegan=vegan)

    # If False, return with corresponding error message
    data_is_valid = validate_data(u1)

    if not data_is_valid[0]:
        return data_is_valid

    # Return True if user added to database, or return False and error message
    result = insert_user(u1, a1)

    return result


def validate_data(user):
    # Check if username is free
    if not is_username_free(user.username):
        return False, 'Username is already taken. Please choose another.'

    # Validate data length
    if len(user.fullname) < 1:
        return False, 'Name is mandatory.'

    if len(user.username) < 5:
        return False, 'Username must have at least 5 characters.'

    if len(user.password) < 5:
        return False, 'Password must have at least 5 characters.'

    if not is_valid_age(user.age):
        return False, 'Invalid age. Please insert valid age.'

    if not is_valid_gender(user.gender):
        return False, 'Invalid gender.'

    return True, ''


def is_valid_gender(gender):
    if gender == 'M' or gender == 'F':
        return True
    return False


def is_field_checked(form, field):
    """ Deprecated. Direct True/False verification used instead. """
    # Checkbox fields come in True/False form
    if field in form:
        if form[field]:
            return True
    return False


def is_valid_age(age):
    # Checks if age field is an integer between 0 and 120
    age = int(age)
    try:
        if age < 0 or age > 120:
            return False
        else:
            return True
    except ValueError:
        return False


