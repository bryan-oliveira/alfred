from flask import render_template, flash, redirect, request, url_for
from app import app
from get_recipes_from_file import getRecipesFromFile, getRecipeByName
from alfred.alfred_brain import alfred_brain
from alfred.registration_logic import register_account, login_account
import random

RECOMMENDED_RECIPE_LIST_SIZE = 8


# Alfred main page
@app.route('/')
@app.route('/index')
def index():
    # Loads recipes from fie JSON format, returns random X at random
    recipes = getRecipesFromFile()

    print len(recipes), " recipes"

    return_recipes = random.sample(recipes, RECOMMENDED_RECIPE_LIST_SIZE)
    return render_template('index.html',
                           title='Home',
                           recipes=return_recipes)


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
    if request.method == 'POST':
        status = login_account(request.form)
        if status[0]:
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error_msg=status[1])

    return render_template('login.html')