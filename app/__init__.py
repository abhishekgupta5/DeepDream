# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_login import LoginManager
from flask_migrate import Migrate

#DB Initializing object
db = SQLAlchemy()

#Login Manager Initializing object
login_manager = LoginManager()

def create_app(config_name):

    #App config details
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    #DB Initialized
    db.init_app(app)

    #Login Manager Initialized
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page"
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)
    from app import models

    return app

