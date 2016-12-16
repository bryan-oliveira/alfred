from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.mail import Mail

# Set up flask environment
app = Flask(__name__)

# Import bcrypt hash utilities for password management
bcrypt = Bcrypt(app)

# Load configuration file
app.config.from_object('config')

lm = LoginManager()
# lm.init_app(app) # Try to fix exception by loading after last statement in this file

# Load SQLAlchemy
db = SQLAlchemy(app)

# Load Flask-Mail
mail = Mail(app)

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
