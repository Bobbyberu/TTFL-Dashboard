from flask import Flask, abort
from app.api_controller import api_controller
from app.db_controller import initialize_database, test, insert_all_boxscores, season_catch_up, insert_all_players
from peewee import *
import time
from urllib import request
from app.services.scheduler import init_scheduler
from app.services.logger import getLogger

if __name__ == 'ttfl_dashboard_api':
    print("""  
  _______ _______ ______ _        _____            _     _                         _ 
 |__   __|__   __|  ____| |      |  __ \          | |   | |                       | |
    | |     | |  | |__  | |      | |  | | __ _ ___| |__ | |__   ___   __ _ _ __ __| |
    | |     | |  |  __| | |      | |  | |/ _` / __| '_ \| '_ \ / _ \ / _` | '__/ _` |
    | |     | |  | |    | |____  | |__| | (_| \__ \ | | | |_) | (_) | (_| | | | (_| |
    |_|     |_|  |_|    |______| |_____/ \__,_|___/_| |_|_.__/ \___/ \__,_|_|  \__,_|                                                                                                                                                
    """)


def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True

    app.register_blueprint(api_controller)

    logger = getLogger(__name__)

    init_scheduler()

    # initialize_database()
    # insert_all_players()
    insert_all_boxscores(2018, 2, 8)
    # parse_all_players()
    # app.run(use_reloader=False)
    return app
