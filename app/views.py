from flask import render_template, redirect, request, url_for, g, flash, abort
from app import app, lm
from get_recipes_from_file import getRecipesFromFile, getRecipeByName
from alfred.alfred_brain import alfred_brain
from alfred.registration_logic import register_account
import random
from app.models import Users
from .forms import LoginForm
from flask.ext.login import login_user, logout_user, login_required, current_user


RECOMMENDED_RECIPE_LIST_SIZE = 8


# Alfred main page
@app.route('/')
@app.route('/index')
def index():

    if current_user.is_authenticated:
        # Loads recipes from fie JSON format, returns random X at random
        recipes = getRecipesFromFile()
        form = LoginForm()
        print len(recipes), "recipes"
        user = current_user.fullname.split()[0]

        return_recipes = random.sample(recipes, RECOMMENDED_RECIPE_LIST_SIZE)
        return render_template('index.html',
                               title='Home',
                               recipes=return_recipes,
                               form=form,
                               user=user)

    else:
        # Loads recipes from fie JSON format, returns random X at random
        recipes = getRecipesFromFile()
        form = LoginForm()
        print len(recipes), " recipes"
        print current_user

        return_recipes = random.sample(recipes, RECOMMENDED_RECIPE_LIST_SIZE)
        return render_template('index.html',
                               title='Home',
                               recipes=return_recipes,
                               form=form)


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
                           title=recipe['name'],
                           recipes=return_recipes,
                           recipe=recipe)


# Upload audio clip to flask | Clicking on Microphone icon triggers this
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # Debug audio BLOB
    # app.logger.debug(request.files['audio'])

    # Get spoken audio clip
    audio = request.files['audio']

    # Send to alfred brain, receive recipes ready to show
    recipes = alfred_brain(audio)

    # print recipes
    print len(recipes)

    # TODO: Change to recommended recipes whenever possible
    # Loads recipes from file (JSON), returns 20 random
    recommend_recipes = getRecipesFromFile()
    return_recipes = random.sample(recommend_recipes, RECOMMENDED_RECIPE_LIST_SIZE)

    return render_template('show_recipe_results.html', recipes=recipes)


# Register view
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        result = register_account(request.form)
        if result[0]:
            # Registered user with success
            return redirect(url_for('index'))
        else:
            return render_template('register.html', error_msg=result[1])

    return render_template('register.html')


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

    return render_template('index.html',
                           title='Sign In',
                           form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('index')


def next_is_valid(url):
    """This function receives an url, and must heck whether it is valid/safe"""
    print url
    return True


@lm.user_loader
def load_user(id_):
    return Users.query.get(int(id_))

