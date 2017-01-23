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
from app.models import User
from app.database.users.db_delete import delete_user
from app.speech.alfred_tts import get_raw_wav
from forms import LoginForm, RegisterForm, ProfileForm, DeleteForm
from app import bcrypt
from email import generate_confirmation_token, confirm_token
from app.database.users import db_query
from email import send_email
from flask import Markup

RECOMMENDED_RECIPE_LIST_SIZE = 8


def getUserName():
    # TODO: Consider stashing everything in session var
    if current_user.is_authenticated:
        return current_user.fullname.split()[0]
    return 'Anonymous'


@app.route('/test')
def test():
    return render_template('thinking_alfred.html')


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
    # if current_user.is_authenticated:

    alfred_voice = None
    alfred_greeting = False
    tooltip = False  # Show help tooltip

    user = getUserName()  # Send first name to template

    # If time var available, check inactivity duration. >10m = Alfred greets you
    if 'time' in session:
        now = datetime.utcnow()
        duration = now - session['time']
        # [#] print>> sys.stderr, "Now:", now, "Stamp:", session['time'], "Duration:", duration

        if duration > timedelta(minutes=10):
            alfred_greeting = True
    else:
        alfred_greeting = True
        tooltip = True

    session['time'] = datetime.utcnow()

    if alfred_greeting:
        phrase = 'Hello ' + user + ', how may I help you?'
        alfred_voice = get_raw_wav(phrase)

    return render_template('categories.html',
                           title='Home',
                           recipe_suggestions=return_recipes,
                           user=user,
                           wavfile=alfred_voice,
                           tooltip=tooltip,
                           login_form=login_form)

    """
    else:
        # [#] print>> sys.stderr, "Current User not auth:", current_user
        tooltip = True
        return render_template('categories.html',
                               title='Home',
                               recipe_suggestions=return_recipes,
                               login_form=login_form,
                               tooltip=tooltip)
    """


# Get recipe by name
@app.route('/search')
def search_recipe(recipe_name=''):
    login_form = LoginForm()

    # Get any args passed through GET|POST
    recipe_search = request.args.get('recipe_name')

    # If there is a GET request user what comes in form, otherwise use recipe_name argument
    if recipe_search is None:
        recipe_search = recipe_name

    # Loads recipes from fie JSON format, returns random 20 at random
    recipes = rs.get_recipes_from_file()
    return_recipes = random.sample(recipes, RECOMMENDED_RECIPE_LIST_SIZE)

    recipe = rs.get_recipe_by_name(recipe_search)

    is_favorite = False

    if current_user.is_authenticated:
        for fav in current_user.favorite:
            # Normalize string comparison, strip whitespace and make lowercase
            if recipe['title'].strip().lower() == fav.title.strip().lower():
                is_favorite = True

    return render_template('recipe_template.html',
                           title=recipe['title'],
                           recipe_suggestions=return_recipes,
                           recipe=recipe,
                           user=getUserName(),
                           login_form=login_form,
                           fav=is_favorite)


@login_required
@app.route('/toggle-is-favorite')
def toggle_is_favorite():
    """ Add/remove recipe from user's favorite recipes list """
    title = request.args.get('recipe_name')
    next = request.args.get('next')
    # print title
    # print next
    db_query.toggle_recipe_is_favorite(current_user.id, title)
    return redirect_url(next, title)


@app.route('/tag/<tag_name>', methods=['GET', 'POST'])
def get_recipes_by_tag(tag_name):

    login_form = LoginForm()
    recipes = rs.get_recipes_by_tag(tag_name)

    if len(recipes) > 23:
        recipes = random.sample(recipes, 12)

    # include_base_template = True, is a switch to include the base-template
    return render_template('show_recipe_results.html',
                           recipes=recipes,
                           user=getUserName(),
                           login_form=login_form,
                           include_base_template=True)


# Upload audio clip to flask
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    login_form = LoginForm()
    # Get spoken audio clip
    audio = request.files['audio']

    # Send first name to show in header
    user = getUserName()

    # Send to alfred brain, receive recipes ready to show
    ingredient_list, recipes, timer_duration = alfred_brain(current_user, audio)

    if len(recipes) > 11:
        recipes = random.sample(recipes, 12)

    # Loads recipes from fie JSON format, returns random 20 at random
    recipe_list = rs.get_recipes_from_file()
    return_recipes = random.sample(recipe_list, RECOMMENDED_RECIPE_LIST_SIZE)

    # Recipe search error message
    err_msg = ''
    print 'Len', len(recipes)
    if len(recipes) == 0:
        err_msg = 'Sorry, no recipes were found for your search terms.'
        ingredient_list = ''

    return render_template('show_recipe_results.html',
                           recipes=recipes,
                           recipe_suggestions=return_recipes,
                           recipe_search_error_msg=err_msg,
                           user=user,
                           login_form=login_form,
                           ingredient_list=ingredient_list,
                           include_base_template=False)


@app.route('/search_keywords', methods=['POST'])
def search_keywords():
    login_form = LoginForm()

    keywords = request.form['keywords']

    ingredient_list, recipes, timer_duration = alfred_brain(current_user, None, keywords)

    if len(recipes) > 11:
        recipes = random.sample(recipes, 12)

    # Send first name to show in header
    user = getUserName()

    # Loads recipes from fie JSON format, returns random 20 at random
    recipe_list = rs.get_recipes_from_file()
    return_recipes = random.sample(recipe_list, RECOMMENDED_RECIPE_LIST_SIZE)

    # Recipe search error message
    err_msg = ''
    if len(recipes) == 0:
        err_msg = 'Sorry, no recipes were found for your search term %s' % keywords

    return render_template('show_recipe_results.html',
                           recipes=recipes,
                           recipe_search_error_msg=err_msg,
                           recipe_suggestions=return_recipes,
                           user=user,
                           login_form=login_form,
                           ingredient_list=ingredient_list,
                           include_base_template=True)


def redirect_url(next, recipe_name=''):
    """ Redirection rules """
    if next == 'search':
        return search_recipe(recipe_name)
    if next == 'favorites':
        return favorites()


@app.route('/test_users', methods=['GET'])
def test_users():
    users = User.query.all()
    send = ''
    for user in users:
        send += 'id:%d fullname:%s username:%s email:%s<br>hash:%s<br>gender:%s age:%d registered on:%s<br>' \
                'admin:%s confirmed:%s confirmed on:%s<br><br>' \
                % (user.id, user.fullname, user.username, user.email,
                   user.password, user.gender, user.age, user.registered_on,
                   user.admin, user.confirmed, user.confirmed_on)

    return send


# Register view
@app.route('/register', methods=['GET', 'POST'])
def register():
    page_title = 'Register an Account'
    form = RegisterForm()
    login_form = LoginForm()

    if form.validate_on_submit():
        # print form.data

        # Register user account
        result = register_account(form)

        # User registered successfully, perform login and redirect to index
        if result[0]:

            # Get user
            """
            # Getting error on register sometimes
            # user = User.query.filter_by(username=form.username.data).first()
            """
            # Using form data instead
            email = form.email.data

            # print user
            token = generate_confirmation_token(email)
            # print token

            confirm_url = url_for('confirm_email', token=token, _external=True)
            # print confirm_url

            html = render_template('emails/activate_account_email.html', confirm_url=confirm_url)
            # print html

            subject = "Please confirm your email"
            send_email(email, subject, html)

            # login_user(user, remember=True)
            flash('Registration successful. A confirmation email has been sent via email.', 'is-success')
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
        username = form.username.data.lower()
        password = form.password.data

        # Find user
        user = User.query.filter_by(username=username).first()

        # print user
        # If user exists
        if user:
            # Check whether password matches hash
            password = bcrypt.check_password_hash(user.get_hash(), password)

            if password:
                login_user(user, remember=True)
                flash('Logged in successfully!', 'is-success')

                # next_ = request.args.get('next')
                # if not next_is_valid(next_):
                #    return abort(400)

                return redirect(url_for('index'))

    flash('Invalid username/password.', 'is-danger')
    return redirect(url_for('index'))


@app.route('/resend', methods=['GET'])
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('emails/activate_account_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    msg = Markup('A new confirmation email has been sent to <strong>%s</strong>.' % current_user.email)
    flash(msg, 'is-info')
    return redirect(url_for('index'))


@login_required
@app.route("/profile", methods=['GET', 'POST'])
def profile_page():
    # Get user name to print in profile page
    user_name = getUserName()

    # Anonymous user is logged, redirect with error message
    if user_name == 'Anonymous':
        flash('Please log in to view profile.')
        return redirect('index')

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
                flash(pwd_status[1], 'is-danger')
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


# TODO: Not a view. Move to application helpers section
def check_password(form):
    """ Check if user's password is correct before changing to a new one. (profile page) """
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


@login_required
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
def confirm_email(token):
    # Check if user is logged in - if not ask to do so first before confirm. Security measure
    if not current_user.is_authenticated:
        flash('Please login in order to verify your account.', 'is-info')
        return redirect(url_for('index'))

    if current_user.confirmed:
        flash('Account already confirmed. Please login.', 'is-success')
        return redirect(url_for('index'))

    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first()
    # print "Find user:", user.fullname

    if user.email == email:
        db_query.confirm_user(user)
        flash('You have confirmed your account. Thanks!', 'is-success')
    else:
        msg = Markup('The confirmation link is invalid or has expired. '
                     '<a href="/resend" style="color:grey; text-decoration: underline;">'
                     '<strong>Click here</strong></a> to resend. ')
        flash(msg, 'is-danger')

    return redirect(url_for('index'))


@login_required
@app.route("/admin", methods=['GET'])
def admin_page():
    return render_template("admin.html")


@login_required
@app.route('/favorites')
def favorites():
    user_name = getUserName()

    # Anonymous user is logged, redirect with error message
    if user_name == 'Anonymous':
        flash('Please log in to view favorites.')
        return redirect('index')

    recipes = []
    for recipe_name in current_user.favorite:
        recipes.append(rs.get_recipe_by_name(recipe_name.title))

    return render_template('favorites.html',
                           title='Home',
                           user=user_name,
                           recipes=recipes,
                           favorite_icon=True)


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


@lm.user_loader
def load_user(id_):
    return User.query.get(int(id_))


# TODO: Not a view. Move to application helpers section
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
