from flask import Flask, abort
from ttfl_dashboard_api.controller import controller
from ttfl_dashboard_api.db_controller import initialize_database, get_ttfl_scores
from peewee import *
import time

app = Flask(__name__)
app.config['TESTING'] = True
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

app.register_blueprint(controller)


if __name__ == "__main__":
    start_time = time.time()
    initialize_database(2018,12,13)
    print("--- %s seconds ---" % (time.time() - start_time))
    app.run(use_reloader=False)
