from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt

# Set up flask environment
app = Flask(__name__)

# Import bcrypt hash utilities for password management
bcrypt = Bcrypt(app)

# Load configuration file
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)

db = SQLAlchemy(app)

from app import views
from app import models

# Include Anonymous user class (models.py)
lm.anonymous_user = models.AnonymousUser
