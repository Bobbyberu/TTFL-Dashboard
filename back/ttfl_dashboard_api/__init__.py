from flask import Flask, abort
from ttfl_dashboard_api.controller import controller
from ttfl_dashboard_api.db_controller import *
from peewee import *

app = Flask(__name__)
app.config['TESTING'] = True
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

app.register_blueprint(controller)


if __name__ == "__main__":
    app.run(use_reloader=False)
