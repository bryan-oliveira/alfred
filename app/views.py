from flask import render_template, redirect, request, url_for, flash, abort
from flask.globals import session
from datetime import datetime, timedelta
from app import app, lm
import get_recipes_from_file as grff
from alfred.alfred_brain import alfred_brain
from alfred.registration_logic import register_account
import random
from app.models import Users, Allergy
from app.database.users.db_insert import edit_user
from .forms import LoginForm, RegisterForm
from flask.ext.login import login_user, logout_user, login_required, current_user
from app.speech.alfred_tts import get_raw_wav
from app.database.users.db_query import get_user_by_id

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

    form = LoginForm()

    # Loads recipes from fie JSON format, returns random X at random
    recipes = grff.getRecipesFromFile()

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
                               form=form,
                               user=user,
                               wavfile=alfred_voice)

    else:
        # [#] print>> sys.stderr, "Current User not auth:", current_user
        return render_template('categories.html',
                               title='Home',
                               recipe_suggestions=return_recipes,
                               form=form)


# Get recipe by name
@app.route('/search')
def search_recipe():
    form = LoginForm()
    # Get any args passed through GET|POST
    recipe_search = request.args.get('recipe_name')

    # Loads recipes from fie JSON format, returns random 20 at random
    recipes = grff.getRecipesFromFile()
    return_recipes = random.sample(recipes, RECOMMENDED_RECIPE_LIST_SIZE)

    recipe = grff.getRecipeByName(recipe_search)

    if recipe is None:
        return render_template('error_page.html')

    return render_template('show_recipe.html',
                           title=recipe['title'],
                           recipe_suggestions=return_recipes,
                           recipe=recipe,
                           user=getUserName(),
                           form=form)


@app.route('/tag/<tag_name>', methods=['GET', 'POST'])
def get_recipes_by_tag(tag_name):
    recipes = grff.get_recipes_by_tag(tag_name)
    recipes = random.sample(recipes, 24)
    return render_template('show_recipe_results.html',
                           recipes=recipes,
                           user=getUserName())


# Upload audio clip to flask | Clicking on Microphone icon triggers this
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # Get spoken audio clip
    audio = request.files['audio']

    # Send first name to show in header
    user = getUserName()

    # Send to alfred brain, receive recipes ready to show
    recipes = alfred_brain(current_user, audio)

    # Loads recipes from fie JSON format, returns random 20 at random
    recipe_list = grff.getRecipesFromFile()
    return_recipes = random.sample(recipe_list, RECOMMENDED_RECIPE_LIST_SIZE)

    return render_template('show_recipe_results.html',
                           recipes=recipes,
                           recipe_suggestions=return_recipes,
                           user=user)


# Register view
@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        # Save user credentials
        username = request.form['username']
        password = request.form['password']

        # Register user account
        result = register_account(request.form)

        # User registered successfully, perform login and redirect to index
        if result[0]:
            user = Users.query.filter_by(username=username, password=password).first()
            login_user(user, remember=True)
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
        else:
            return render_template('user_template.html', error_msg=result[1], form=form)

    return render_template('user_template.html', form=form, url=url_for('register'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # validate_on_submit runs all validation specs defined in forms.py and returns
    # true if data is valid, safe and ready for processing
    username = form.username.data
    password = form.password.data

    # Loads recipes from fie JSON format, returns random 20 at random
    recipe_list = grff.getRecipesFromFile()
    return_recipes = random.sample(recipe_list, RECOMMENDED_RECIPE_LIST_SIZE)

    if form.validate_on_submit():
        user = Users.query.filter_by(username=username, password=password).first()

        if user is not None:
            login_user(user, remember=True)
            flash('Logged in successfully!')

            next_ = request.args.get('next')

            if not next_is_valid(next_):
                return abort(400)

            return redirect(url_for('index'))

    flash('Invalid username/password.', 'error')
    return render_template('categories.html',
                           title='Sign In',
                           form=form,
                           recipe_suggestions=return_recipes)


@app.route("/profile", methods=['GET', 'POST'])
def profile_page():

    form = RegisterForm()

    if form.validate_on_submit():
        print "Form submitted success"
        user, allergy = get_user_by_id(current_user.id)
        allergy = Allergy()
        form.populate_obj(user)
        form.populate_obj(allergy)
        edit_user(user, allergy)
        return render_template("user_template.html",
                               form=form,
                               user=getUserName(),
                               url=url_for('profile_page'))
    else:
        # Error validating form, reload form
        print "Form submitted error OR GET request"
        print form.errors
        user, allergy = get_user_by_id(current_user.id)
        form = RegisterForm(obj=user)
        form.populate_obj(user)
        # Populate form with object data
        populate_form(form, user, allergy)
        pass

    return render_template("profile.html", form=form, user=getUserName(), url=url_for('profile_page'))


@app.route("/admin", methods=['GET'])
def admin_page():
    return render_template("admin.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('index')


def next_is_valid(url):
    """This function receives an url, and must check whether it is valid/safe"""
    # [#] print>> sys.stderr, "######", url
    return True


@lm.user_loader
def load_user(id_):
    return Users.query.get(int(id_))


def populate_form(form, user, allergy):
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

