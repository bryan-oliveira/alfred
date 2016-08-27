import os

basedir = os.path.abspath(os.path.dirname(__file__))

RECIPE_FILE = os.path.join(basedir, 'recipe_data/recipe.data')
NEW_RECIPE_FILE = os.path.join(basedir, 'recipe_data/new_recipe.data')

UPLOAD_FOLDER = os.path.join(basedir, "audio/")
ROOT_FOLDER = '.'

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

ROOT_FOLDER = ROOT_FOLDER
UPLOAD_FOLDER = UPLOAD_FOLDER
RECIPE_FILE = RECIPE_FILE
NEW_RECIPE_FILE = NEW_RECIPE_FILE

