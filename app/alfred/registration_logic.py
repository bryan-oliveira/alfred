from db.sqlalchemy_query import is_username_free, check_credentials
from db.alfred_db import Users, Allergy
from db.sqlalchemy_insert import insert_user


def register_account(form):
    print 'Registering new Account'
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

    # If False, return it and corresponding error message
    data_is_valid = validate_data(u1)
    if not data_is_valid[0]:
        return data_is_valid

    # Return True if user added to database, or return False and error message
    result = insert_user(u1, a1)
    return result[0]


def validate_data(user):
    # Check if username is free
    if not is_username_free(user.username):
        return False, 'Username is already taken. Please choose another.'

    # Check if all mandatory fields are filled
    field_completion = are_mandatory_fields_filled(user)
    return field_completion


def is_field_checked(form, field):
    # HTML Checkbox fields come in on/off form. This function converts on/off to True/False equivalent
    if field in form:
        if form[field] == 'on':  # Redundant ?
            return True
    return False


def are_mandatory_fields_filled(user):
    if len(user.fullname) < 1:
        return False, 'Name is mandatory.'

    if len(user.username) < 5:
        return False, 'Username must have at least 5 characters.'

    if len(user.password) < 5:
        return False, 'Password must have at least 5 characters.'

    return True, ''


def check_valid_age(form, field):
    # Checks if age field is an integer between 0 and 130
    if field in form:
        try:
            if int(form[field]) < 0 or int(form[field]) > 120:
                return False, 'Invalid Age. Please insert valid age.'
            else:
                return form[field], ''
        except ValueError:
            return -1, ''
    return True, ''


def login_account(form):
    return check_credentials(form['username'], form['pwd'])
