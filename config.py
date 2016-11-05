import os

# Application root path
basedir = os.path.abspath(os.path.dirname(__file__))

# Recipe data files
# RECIPE_FILE = os.path.join(basedir, 'data/recipe.data')
RECIPE_FILE = os.path.join(basedir, 'data/recipes_epicurious.data')

# Ingredient data files
INGREDIENT_TRANSLATION_FILE = os.path.join(basedir, 'ingredientDB.dat')

# Audio file upload folder
UPLOAD_FOLDER = os.path.join(basedir, "data/audio/")

# Flask securty settings
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

" SQLAlchemy data"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False


INGREDIENT_TRANSLATION_FILE = INGREDIENT_TRANSLATION_FILE
UPLOAD_FOLDER = UPLOAD_FOLDER
RECIPE_FILE = RECIPE_FILE


