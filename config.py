import os

# Application root path
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = None
SQLALCHEMY_MIGRATE_REPO = None


class Config(object):
    # Dev mode
    DEBUG = True

    # Flask securty settings
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'hb3WQ34rmDs232'

    # Email token generator
    SECURITY_PASSWORD_SALT = 'dsDds3fFDd23'

    # SQLAlchemy data
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir + '/data', 'database.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    # Flask security settings
    WTF_CSRF_ENABLED = False

    # SQLAlchemy data
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir + '/data', 'test.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'test_migration')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    WTF_CSRF_ENABLED = True

    # Bcrypt algorithm strength for production
    BCRYPT_LOG_ROUNDS = 13


# Data files
DATA_FOLDER = os.path.join(basedir, 'data/')

# Log directory
LOG_FOLDER = os.path.join(basedir, 'log/')

# Recipe data files
# RECIPE_FILE = os.path.join(basedir, 'data/recipe.data')
RECIPE_FILE = os.path.join(basedir, 'data/recipes_epicurious.data')

# Recipe file indexes
PESCATARIAN_RECIPES = os.path.join(DATA_FOLDER, 'pescatarian_recipes.dat')

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
MEAT_POULTRY_DB = os.path.join(DATA_FOLDER, 'meat_poultry_db.dat')
FISH_DB = os.path.join(DATA_FOLDER, 'fish_db.dat')
SEAFOOD_DB = os.path.join(DATA_FOLDER, 'seafood_db.dat')
SPICES_DB = os.path.join(DATA_FOLDER, 'spices_db.dat')
ADDITIONAL_INGS_DB = os.path.join(DATA_FOLDER, 'additional_ingredients_db.dat')
TAG_DB = os.path.join(DATA_FOLDER, 'tag_db.dat')

# Audio file upload folder
UPLOAD_FOLDER = os.path.join(basedir, "data/audio/")

# UPLOAD_FOLDER = UPLOAD_FOLDER
# RECIPE_FILE = RECIPE_FILE
# DATA_FOLDER = DATA_FOLDER

# Logging
RECIPE_REQUESTS_LOG = os.path.join(LOG_FOLDER, 'recipe_requests.log')

# Default Debug mode
DEBUG = False
