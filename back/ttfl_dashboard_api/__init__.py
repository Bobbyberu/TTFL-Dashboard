from flask import Flask, abort
from ttfl_dashboard_api.api_controller import api_controller
from ttfl_dashboard_api.db_controller import initialize_database, test, insert_all_boxscores, season_catch_up, insert_all_players
from peewee import *
import time
from urllib import request
from services.parser import parse_all_players

app = Flask(__name__)
app.config['TESTING'] = True
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

app.register_blueprint(api_controller)


if __name__ == "__main__":
    start_time = time.time()
    # initialize_database()
    # insert_all_players()
    # insert_all_boxscores(2018,12,25)
    # parse_all_players()
    print("--- %s seconds ---" % (time.time() - start_time))
    app.run(use_reloader=False)
