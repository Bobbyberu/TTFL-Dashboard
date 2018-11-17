from flask import Blueprint, url_for, abort
from nba_api.stats.endpoints import commonallplayers

controller = Blueprint('controller', __name__)
api = '/api'

@controller.route('/hello')
def hello():
    return url_for('test')

@controller.route(api)
def apiFunction():
    abort(404)

@controller.route(api + '/allplayers')
def allPlayers():
    return commonallplayers.CommonAllPlayers('1', '00', '2018-19').get_json()