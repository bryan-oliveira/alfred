from flask import render_template, redirect, request, url_for, g, flash, abort
from flask.globals import session
from datetime import datetime, timedelta
from app import app, lm
from get_recipes_from_file import getRecipesFromFile, getRecipeByName
from alfred.alfred_brain import alfred_brain
from alfred.registration_logic import register_account
import random
from app.models import Users
from .forms import LoginForm
from flask.ext.login import login_user, logout_user, login_required, current_user
from app.speech.alfred_tts import get_raw_wav


RECOMMENDED_RECIPE_LIST_SIZE = 8


def getUserName():
    # TODO: Consider stashing everything in session var
    if current_user.is_authenticated:
        return current_user.fullname.split()[0]
    return None


# Alfred main page
@app.route('/')
@app.route('/index')
def index():

    print "Debug:", session

    # If user is authenticated
    if current_user.is_authenticated:

        alfred_voice = None
        alfred_greeting = False

        # Loads recipes from fie JSON format, returns random X at random
        recipes = getRecipesFromFile()

        # Send first name to template
        user = getUserName()

        # If time var available, check inactivity duration. >10m = Alfred greets you
        if 'time' in session:
            now = datetime.utcnow()
            duration = now - session['time']
            print "Now:", now, "Stamp:", session['time'], "Duration:", duration

            if duration > timedelta(minutes=10):
                alfred_greeting = True
        else:
            alfred_greeting = True

        session['time'] = datetime.utcnow()

        if alfred_greeting:
            phrase = 'Hello ' + user + ', how may I help you?'
            print phrase
            alfred_voice = get_raw_wav(phrase)

        return_recipes = random.sample(recipes, RECOMMENDED_RECIPE_LIST_SIZE)

        print "DEBUG:", return_recipes[0]['title']

        return render_template('categories.html',
                               title='Home',
                               recipe_suggestions=return_recipes,
                               form=getForm(),
                               user=user,
                               wavfile=alfred_voice)

    else:
        # Loads recipes from fie JSON format, returns random X at random
        recipes = getRecipesFromFile()

        print "Current User not auth:", current_user

        return_recipes = random.sample(recipes, RECOMMENDED_RECIPE_LIST_SIZE)
        return render_template('categories.html',
                               title='Home',
                               recipe_suggestions=return_recipes,
                               form=getForm())


# Get recipe by name
@app.route('/search')
def search_recipe():

    # Get any args passed through GET|POST
    recipe_search = request.args.get('recipe_name')

    # Loads recipes from fie JSON format, returns random 20 at random
    recipes = getRecipesFromFile()
    return_recipes = random.sample(recipes, RECOMMENDED_RECIPE_LIST_SIZE)

    recipe = getRecipeByName(recipe_search)

    if recipe is None:
        return render_template('error_page.html')

    return render_template('show_recipe.html',
                           title=recipe['title'],
                           recipe_suggestions=return_recipes,
                           recipe=recipe,
                           user=getUserName(),
                           form=getForm())


def getForm():
    return LoginForm()


# Upload audio clip to flask | Clicking on Microphone icon triggers this
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print "Client Sendin Audio --- Starting Upload"
    # Get spoken audio clip
    audio = request.files['audio']

    # Send to alfred brain, receive recipes ready to show
    recipes = alfred_brain(audio)

    # TODO: Scalability: call getRecipesFromFile once and share it to session var; Update every 5m vs every call;
    # Loads recipes from fie JSON format, returns random 20 at random
    recipe_list = getRecipesFromFile()
    return_recipes = random.sample(recipe_list, RECOMMENDED_RECIPE_LIST_SIZE)

    return render_template('show_recipe_results.html',
                           recipes=recipes,
                           recipe_suggestions=return_recipes,
                           user=getUserName())


# Register view
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        result = register_account(request.form)
        if result[0]:
            # Registered user with success
            return redirect(url_for('index'))
        else:
            return render_template('register.html', error_msg=result[1], form=getForm())

    return render_template('register.html', form=getForm())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # validate_on_submit runs all validation specs defined in forms.py and returns
    # true if data is valid, safe and ready for processing
    print form.username.data, form.password.data

    username = form.username.data
    password = form.password.data

    if form.validate_on_submit():
        user = Users.query.filter_by(username=username, password=password).first()
        print user
        if user is None:
            # TODO: Implement message flashing in main index page
            flash('Username or Password is invalid')
            return redirect(url_for('index'))

        login_user(user, remember=True)

        flash('Logged in successfully!')
        print 'Logged in successfully!'

        next_ = request.args.get('next')

        if not next_is_valid(next_):
            print "abort!!!"
            return abort(400)

        return redirect(url_for('index'))

    return render_template('categories.html',
                           title='Sign In',
                           form=form)


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
    print "######", url
    return True


@lm.user_loader
def load_user(id_):
    return Users.query.get(int(id_))

