import random
from datetime import datetime, timedelta
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.globals import session
import database.recipes.recipe_search as rs
from alfred.alfred_brain import alfred_brain
from alfred.registration_logic import register_account
from app import app, lm
from app.database.users.db_insert import edit_user
from app.database.users.db_query import get_user_by_id
from app.models import User, Allergy
from app.database.users.db_delete import delete_user
from app.speech.alfred_tts import get_raw_wav
from .forms import LoginForm, RegisterForm, ProfileForm, DeleteForm
from app import bcrypt
from email_token import generate_confirmation_token, confirm_token
from app.database.users import db_query
from flask.ext.mail import Message
from app import mail

RECOMMENDED_RECIPE_LIST_SIZE = 8


def getUserName():
    # TODO: Consider stashing everything in session var
    if current_user.is_authenticated:
        return current_user.fullname.split()[0]
    return 'Anonymous'


@app.route('/test')
def test():
    pass


# Alfred main page
@app.route('/')
@app.route('/index')
def index():

    login_form = LoginForm()

    # Loads recipes from fie JSON format, returns random X at random
    recipes = rs.get_recipes_from_file()

    # Randomize suggested recipes
    return_recipes = random.sample(recipes, RECOMMENDED_RECIPE_LIST_SIZE)

    # If user is authenticated
    if current_user.is_authenticated:

        alfred_voice = None
        alfred_greeting = False

        # Send first name to template
        user = getUserName()

        # If time var available, check inactivity duration. >10m = Alfred greets you
        if 'time' in session:
            now = datetime.utcnow()
            duration = now - session['time']
            # [#] print>> sys.stderr, "Now:", now, "Stamp:", session['time'], "Duration:", duration

            if duration > timedelta(minutes=10):
                alfred_greeting = True
        else:
            alfred_greeting = True

        session['time'] = datetime.utcnow()

        if alfred_greeting:
            phrase = 'Hello ' + user + ', how may I help you?'
            alfred_voice = get_raw_wav(phrase)

        return render_template('categories.html',
                               title='Home',
                               recipe_suggestions=return_recipes,
                               user=user,
                               wavfile=alfred_voice)

    else:
        # [#] print>> sys.stderr, "Current User not auth:", current_user
        return render_template('categories.html',
                               title='Home',
                               recipe_suggestions=return_recipes,
                               login_form=login_form)


# Get recipe by name
@app.route('/search')
def search_recipe():
    login_form = LoginForm()
    # Get any args passed through GET|POST
    recipe_search = request.args.get('recipe_name')

    # Loads recipes from fie JSON format, returns random 20 at random
    recipes = rs.get_recipes_from_file()
    return_recipes = random.sample(recipes, RECOMMENDED_RECIPE_LIST_SIZE)

    recipe = rs.get_recipe_by_name(recipe_search)

    if recipe is None:
        return render_template('error_page.html')

    return render_template('show_recipe.html',
                           title=recipe['title'],
                           recipe_suggestions=return_recipes,
                           recipe=recipe,
                           user=getUserName(),
                           login_form=login_form)


@app.route('/tag/<tag_name>', methods=['GET', 'POST'])
def get_recipes_by_tag(tag_name):
    login_form = LoginForm()
    recipes = rs.get_recipes_by_tag(tag_name)
    if len(recipes) > 23:
        recipes = random.sample(recipes, 24)
    return render_template('show_recipe_results.html',
                           recipes=recipes,
                           user=getUserName(),
                           login_form=login_form)


# Upload audio clip to flask | Clicking on Microphone icon triggers this
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    login_form = LoginForm()
    # Get spoken audio clip
    audio = request.files['audio']

    # Send first name to show in header
    user = getUserName()

    # Send to alfred brain, receive recipes ready to show
    recipes = alfred_brain(current_user, audio)

    # Loads recipes from fie JSON format, returns random 20 at random
    recipe_list = rs.get_recipes_from_file()
    return_recipes = random.sample(recipe_list, RECOMMENDED_RECIPE_LIST_SIZE)

    return render_template('show_recipe_results.html',
                           recipes=recipes,
                           recipe_suggestions=return_recipes,
                           user=user,
                           login_form=login_form)


# Register view
@app.route('/register', methods=['GET', 'POST'])
def register():
    page_title = 'Register an Account'
    form = RegisterForm()
    login_form = LoginForm()

    if form.validate_on_submit():

        # print form.data

        # Register user account
        result = register_account(request.form)

        # User registered successfully, perform login and redirect to index
        if result[0]:
            # Get user
            user = User.query.filter_by(username=form.username.data).first()

            # print user

            login_user(user, remember=True)
            flash('Registration successful!', 'is-success')
            return redirect(url_for('index'))
        else:
            error_msg = result[1]
            flash(error_msg, 'is-danger')
            return render_template('user_info_template.html',
                                   form=form,
                                   login_form=login_form,
                                   title=page_title)

    return render_template('user_info_template.html',
                           form=form,
                           login_form=login_form,
                           url=url_for('register'),
                           title=page_title)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        # Get login credentials
        username = form.username.data
        password = form.password.data

        # Find user
        user = User.query.filter_by(username=username).first()

        # print user

        # If exists and already confirmed email
        if user:
            if user.confirmed:
                # Check whether password matches hash
                password = bcrypt.check_password_hash(user.get_hash(), password)

                if password:
                    login_user(user, remember=True)
                    flash('Logged in successfully!', 'is-success')

                    # next_ = request.args.get('next')
                    # if not next_is_valid(next_):
                    #    return abort(400)

                    return redirect(url_for('index'))

            flash('Please confirm email to login with this account.', 'is-info')

    flash('Invalid username/password.', 'is-danger')
    return redirect(url_for('index'))


@login_required
@app.route("/profile", methods=['GET', 'POST'])
def profile_page():

    # Get user name to print in profile page
    user_name = getUserName()

    # Create profile page title with user name
    page_title = user_name + '\'s Account Settings'

    # Get user object
    user, allergy = get_user_by_id(current_user.id)

    form = ProfileForm()
    delete_form = DeleteForm()

    if request.method == 'GET':
        # Fill form with user data
        form = ProfileForm(request.form, obj=user)

        # Fill form with extra allergy data
        populate_form_with_allergy_data(form, allergy)

    if form.validate_on_submit():
        pwd_status = check_password(form)

        # Check for password changes
        if form.password.data != '' or form.new_password.data != '' or form.new_password_conf.data != '':
            # print "Changing password."

            if not pwd_status[0]:
                # print "Passwords dont match"
                flash( pwd_status[1], 'is-danger')
                return render_template("profile.html",
                                       form=form,
                                       delete_form=delete_form,
                                       user=user_name,
                                       url=url_for('profile_page'),
                                       title=page_title)

        # Commit changes to object if updates were made. Compare object with form
        # pwd_status is a tuple (boolean, error message). If boolean is True, edit_user
        # will also perform an update of the user's password
        updates_made = edit_user(user, form, pwd_status[0])

        if updates_made == True:
            flash('Profile updated successfully!', 'is-success')

    return render_template("profile.html",
                           form=form,
                           delete_form=delete_form,
                           user=user_name,
                           url=url_for('profile_page'),
                           title=page_title)


def check_password(form):
    # Check if old password field in profile page matches saved hash
    old_pwd = bcrypt.check_password_hash(current_user.password, form.password.data)
    if old_pwd:
        # Check if new password and confirmation password match
        if form.new_password.data == form.new_password_conf.data:
            # Password validators are optional. This allows to have password fields empty
            # and still be able to submit form with out constantly inserting a password.
            # Therefore, if old password was submitted, and new passwords match. Make
            # sure length is in range (6,30)
            if 5 < len(form.new_password.data) < 31:
                return True, 'Success'
            return False, 'New password must contain at least 6 characters.'
        return False, 'New passwords do not match. Please try again.'
    return False, 'Current password is wrong. Please try again.'


@app.route('/delete_account', methods=['POST'])
def delete_account():

    form = DeleteForm()
    password = form.password.data
    user = User.query.get(current_user.id)

    if user:
        if bcrypt.check_password_hash(user.password, password):
            # Log user off
            logout_user()

            # Delete user from db
            delete_user(user)

            # Confirm delete operation and redirect to index
            flash('Your account has been canceled.', 'is-info')
            return redirect('index')

    # Either wrong password or user doesn't exist
    flash('Invalid password. Please enter your password to delete this account.', 'is-danger')
    return redirect(url_for('profile_page'))


@app.route('/confirm/<token>')
# @login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'is-danger')

    user = User.query.filter_by(email=email).first_or_404()

    if user.confirmed:
        flash('Account already confirmed. Please login.', 'is-info')
    else:
        db_query.confirm_user(user)
        flash('You have confirmed your account. Thanks!', 'is-success')
    return redirect(url_for('index'))


@app.route("/admin", methods=['GET'])
def admin_page():
    return render_template("admin.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully!', 'is-success')
    return redirect('index')


def next_is_valid(url):
    """This function receives an url, and must check whether it is valid/safe"""
    # [#] print>> sys.stderr, "######", url
    return True


@app.route('/send_mail')
def send_mail():
    # print "Sending mail."
    msg = Message()
    msg.recipients = ['vicdaruf@yahoo.com']
    msg.sender = ('Alfred', 'alfred@alfred.com')
    msg.body = "Hello. This is the body."
    mail.send(msg)


@lm.user_loader
def load_user(id_):
    return User.query.get(int(id_))


def populate_form_with_allergy_data(form, allergy):
    form.lowchol.data = allergy.lowchol
    form.highchol.data = allergy.highchol
    form.underw.data = allergy.underw
    form.overw.data = allergy.overw
    form.gluten.data = allergy.gluten
    form.nuts.data = allergy.nuts
    form.fish.data = allergy.fish
    form.sesame.data = allergy.sesame
    form.vegetarian.data = allergy.vegetarian
    form.vegan.data = allergy.vegan

