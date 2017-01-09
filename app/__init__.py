from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.mail import Mail
import os
# Set up flask environment
app = Flask(__name__)

# Get environment (TESTING, DEVELOPMENT, PRODUCTION)
if 'APP_SETTINGS' in os.environ:
    config_mode = os.environ['APP_SETTINGS']
else:
    config_mode = 'DEVELOPMENT'

# Load configuration file
if config_mode == 'TESTING':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.Config')

##############
# Extensions #
##############

# Import bcrypt hash utilities for password management
bcrypt = Bcrypt(app)

lm = LoginManager()
# lm.init_app(app) # Try to fix exception by loading after last statement in this file

# Load SQLAlchemy
db = SQLAlchemy(app)

# Load Flask-Mail
mail = Mail(app)

# Mail configs
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False

from app import views
from app import models

# Include Anonymous user class (models.py)
lm.anonymous_user = models.AnonymousUser
lm.init_app(app)
