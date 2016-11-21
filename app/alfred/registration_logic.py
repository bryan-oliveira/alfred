from app.database.users.db_query import is_username_free
from app.database.users.db_insert import insert_user
from app.models import Users, Allergy
import sys


debug_mode = False


def register_account(form):
    print >> sys.stderr, 'Registering new Account'
    fullname = form['fullname']
    username = form['username']
    pwd = form['pwd']

    # Optional Fields
    age = check_valid_age(form, 'age')
    if not age[0]:  # If age False, return error
        return age

    age = age[0]  # Strip error message

    gender = 'M'

    milk = is_field_checked(form, 'milk')
    eggs = is_field_checked(form, 'eggs')
    soy = is_field_checked(form, 'soy')
    nuts = is_field_checked(form, 'nuts')
    fish = is_field_checked(form, 'fish')
    sesame = is_field_checked(form, 'sesame')
    gluten = is_field_checked(form, 'gluten')

    u1 = Users(fullname=fullname, username=username, age=age, gender=gender, password=pwd)
    a1 = Allergy(soy=soy, milk=milk, eggs=eggs, nuts=nuts, gluten=gluten, fish=fish, sesame=sesame)

    # If False, return with corresponding error message
    data_is_valid = validate_data(u1)
    if debug_mode:
        print >> sys.stderr, "register_account<data_is_valid: ", data_is_valid

    if not data_is_valid[0]:
        if debug_mode:
            print >> sys.stderr, "register_account<data_is_valid<inside IF>: ", data_is_valid
        return data_is_valid

    # Return True if user added to database, or return False and error message
    result = insert_user(u1, a1)
    if debug_mode:
        print >> sys.stderr, "register_account>result:", result
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

    return True, ''


def is_field_checked(form, field):
    # HTML Checkbox fields come in on/off form. This function converts on/off to True/False equivalent
    if field in form:
        if form[field] == 'on':  # Redundant ?
            return True
    return False


def check_valid_age(form, field):
    # Checks if age field is an integer between 0 and 120
    if field in form:
        try:
            if int(form[field]) < 0 or int(form[field]) > 120:
                print >> sys.stderr, "check_valid_age: False. Invalid age. Please insert valid age."
                return False, 'Invalid age. Please insert valid age.'
            else:
                # Returns age
                print >> sys.stderr, "check_valid_age:", form[field]
                return form[field], ''
        except ValueError:
            print >> sys.stderr, "check_valid_age: False."
            return False, 'Invalid age. Please try again'

    print >> sys.stderr, "Should never reach here. But then again..."
    return False, ''

