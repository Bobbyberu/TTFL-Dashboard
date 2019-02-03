from flask import Flask, abort
from flask_script import Manager, Server
from ttfl_dashboard_api.api_controller import api_controller
from ttfl_dashboard_api.db_controller import initialize_database, test, insert_all_boxscores, season_catch_up, insert_all_players
from peewee import *
import time
from urllib import request
from services.scheduler import init_scheduler
from services.logger import getLogger

start_time = time.time()

if __name__ == 'ttfl_dashboard_api':
    print("""  
  _______ _______ ______ _        _____            _     _                         _ 
 |__   __|__   __|  ____| |      |  __ \          | |   | |                       | |
    | |     | |  | |__  | |      | |  | | __ _ ___| |__ | |__   ___   __ _ _ __ __| |
    | |     | |  |  __| | |      | |  | |/ _` / __| '_ \| '_ \ / _ \ / _` | '__/ _` |
    | |     | |  | |    | |____  | |__| | (_| \__ \ | | | |_) | (_) | (_| | | | (_| |
    |_|     |_|  |_|    |______| |_____/ \__,_|___/_| |_|_.__/ \___/ \__,_|_|  \__,_|                                                                                                                                                
    """)


app = Flask(__name__)
app.config['TESTING'] = True
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

app.register_blueprint(api_controller)

logger = getLogger(__name__)


if __name__ == "__main__":
    init_scheduler()
    # initialize_database()
    # insert_all_players()
    # insert_all_boxscores(2018,12,25)
    # parse_all_players()
    logger.info("TTFLDashboard started in %s seconds" %
                (time.time() - start_time))
    app.run(use_reloader=False)
