from flask import Flask, abort
from app.api_controller import api_controller
import time
from urllib import request
from app.db_models import db
from app.db_controller import populate_database, season_catch_up
from app.services.scheduler import init_scheduler
from app.services.logger import getLogger
from config import PROD_DATABASE, UNIT_TEST_DATABASE


def wipe_db(db):
    """
    Drop all db tables and recreate clean db
    """
    logger = getLogger(__name__)
    db.drop_all()
    logger.info('Database successfully dropped!')
    db.create_all()
    logger.info('Database successfully created!')


def create_app():
    """
    Create app to launch application
    """
    app = Flask(__name__)
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True

    # config database
    app.config['SQLALCHEMY_DATABASE_URI'] = PROD_DATABASE
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    db.app = app
    app.register_blueprint(api_controller)

    init_scheduler()

    return app


def create_app_test():
    """
    Create flask app to launch unit tests
    """
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['ENV'] = 'development'
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["DEBUG"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = UNIT_TEST_DATABASE

    # config database
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.register_blueprint(api_controller)
    return app
