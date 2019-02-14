from flask import Flask, abort
from app.api_controller import api_controller
from peewee import *
import time
from urllib import request
from app.db_models import db
from app.services.scheduler import init_scheduler
from app.services.logger import getLogger
from config import TEST_DATABASE, PROD_DATABASE


def create_app():
    logger = getLogger(__name__)

    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True

    # config database
    app.config['SQLALCHEMY_DATABASE_URI'] = PROD_DATABASE
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    db.app = app
    app.register_blueprint(api_controller)

    init_scheduler()

    """db.drop_all()
    logger.info('Database successfully dropped!')
    db.create_all()
    logger.info('Database successfully created!')"""
    return app
