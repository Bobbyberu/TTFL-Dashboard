from flask import Flask, abort
from ttfl_dashboard_api.controller import controller
from ttfl_dashboard_api.db_controller import create_tables, insert_all_teams, insert_all_players, insert_all_games, get_all_games, insert_all_boxscores, get_ttfl_scores
from peewee import *

app = Flask(__name__)
app.config['TESTING'] = True
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

app.register_blueprint(controller)


if __name__ == "__main__":
    create_tables()
    app.run(use_reloader=False)
