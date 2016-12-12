from app.database.users.db_query import is_username_free
from app.database.users.db_insert import insert_user
from app.models import Users, Allergy
import sys


debug_mode = False


def register_account(form):
    # User information
    fullname = form['fullname']
    username = form['username']
    pwd = form['pwd']
    age = form['age']
    gender = form['gender']

    # Allergies/Restrictions
    lowchol = is_field_checked(form, 'lowchol')
    highchol = is_field_checked(form, 'highchol')
    overw = is_field_checked(form, 'overw')
    underw = is_field_checked(form, 'underw')
    nuts = is_field_checked(form, 'nuts')
    fish = is_field_checked(form, 'fish')
    sesame = is_field_checked(form, 'sesame')
    gluten = is_field_checked(form, 'gluten')
    vegetarian = is_field_checked(form, 'vegetarian')
    vegan = is_field_checked(form, 'vegan')

    u1 = Users(fullname=fullname, username=username, age=age, gender=gender, password=pwd)
    a1 = Allergy(lowchol=lowchol, highchol=highchol, overw=overw, underw=underw, nuts=nuts,
                 gluten=gluten, fish=fish, sesame=sesame)

    # If False, return with corresponding error message
    data_is_valid = validate_data(u1)
    if debug_mode:
        print "register_account<data_is_valid: ", data_is_valid

    if not data_is_valid[0]:
        if debug_mode:
            print "register_account<data_is_valid<inside IF>: ", data_is_valid
        return data_is_valid

    # Return True if user added to database, or return False and error message
    result = insert_user(u1, a1)

    if debug_mode:
        print sys.stderr, "register_account>result:", result

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
    if gender == 'Male' or gender == 'Female':
        return True
    return False


def is_field_checked(form, field):
    # HTML Checkbox fields come in on/off form. This function converts on/off to True/False equivalent
    if field in form:
        if form[field] == 'on':  # Redundant ?
            return True
    return False


def is_valid_age(age):
    # Checks if age field is an integer between 0 and 120
    age = int(age)
    print age
    try:
        if age < 0 or age > 120:
            return False
        else:
            return True
    except ValueError:
        return False


