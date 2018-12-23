from flask import Flask, abort
from ttfl_dashboard_api.api_controller import api_controller
from ttfl_dashboard_api.db_controller import initialize_database, get_ttfl_scores, test, get_all_boxscores
from peewee import *
import time

app = Flask(__name__)
app.config['TESTING'] = True
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

app.register_blueprint(api_controller)


if __name__ == "__main__":
    #start_time = time.time()
    #initialize_database(2018, 12, 22)
    #print("--- %s seconds ---" % (time.time() - start_time))
    #test()
    app.run(use_reloader=True)