import os

# Application root path
basedir = os.path.abspath(os.path.dirname(__file__))

# Log directory
LOG_FOLDER = os.path.join(basedir, 'log/')

# Recipe data files
# RECIPE_FILE = os.path.join(basedir, 'data/recipe.data')
RECIPE_FILE = os.path.join(basedir, 'data/recipes_epicurious.data')

# Data files
DATA_FOLDER = os.path.join(basedir, 'data/')

# USDA Food Info Files
USDA_FOLDER = os.path.join(DATA_FOLDER, 'usda_food_info')

# USDA files
USDA_VEGETABLE_DATA = os.path.join(USDA_FOLDER, 'usda_veggies.dat')
USDA_FRUIT_DATA = os.path.join(USDA_FOLDER, 'usda_fruits.dat')
USDA_DAIRY_DATA = os.path.join(USDA_FOLDER, 'usda_dairy.dat')
USDA_SPICES_DATA = os.path.join(USDA_FOLDER, 'usda_spices.dat')
USDA_LEGUMES_DATA = os.path.join(USDA_FOLDER, 'usda_legumes.dat')

# Ingredient data files
VEGETABLE_DB = os.path.join(DATA_FOLDER, 'veggie_db.dat')
FRUIT_DB = os.path.join(DATA_FOLDER, 'fruit_db.dat')

# Audio file upload folder
UPLOAD_FOLDER = os.path.join(basedir, "data/audio/")

# Flask securty settings
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# SQLAlchemy data
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir + '/data', 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = UPLOAD_FOLDER
RECIPE_FILE = RECIPE_FILE
DATA_FOLDER = DATA_FOLDER

# Logging
RECIPE_REQUESTS_LOG = os.path.join(LOG_FOLDER, 'recipe_requests.log')

# Dev mode
DEBUG = False
