import json
from flask import Blueprint, url_for, abort, jsonify, Response
from db_controller import get_all_boxscores

api_controller = Blueprint('api_controller', __name__)
api = '/api'


@api_controller.route(api)
def apiFunction():
    abort(404)


@api_controller.route(api+'/boxscores/<int:year>/<int:month>/<int:day>')
def get_boxscores(year: int, month: int, day: int):
    all_boxscores = get_all_boxscores(year, month, day)
    json_respose = json.dumps([boxscore.__dict__['__data__']
                               for boxscore in all_boxscores])
    response = Response(
        response=json_respose,
        status=200,
        mimetype='application/json'
    )
    return response
