import json
from flask import Blueprint, url_for, abort, jsonify, Response
from db_controller import get_all_boxscores, get_all_players

api_controller = Blueprint('api_controller', __name__)
api = '/api'


@api_controller.route(api)
def apiFunction():
    abort(404)


@api_controller.route(api+'/players')
def get_players():
    all_players = get_all_players()
    # json_response = json.dumps([player.__dict__['__data__']
    #                           for player in all_players])
    json_response = build_valid_json(
        [player.__dict__['__data__'] for player in all_players])
    response = Response(
        response=json_response,
        status=200,
        mimetype='application/json'
    )
    return response


@api_controller.route(api+'/boxscores/<int:year>/<int:month>/<int:day>')
def get_boxscores(year: int, month: int, day: int):
    all_boxscores = get_all_boxscores(year, month, day)
    if all_boxscores is None:
        json_response = build_error_json(
            "Impossible to get boxscores with a date in the future")
        status = 403
    else:
        json_response = json.dumps([boxscore.__dict__['__data__']
                                    for boxscore in all_boxscores])
        status = 200
    response = Response(
        response=json_response,
        status=status,
        mimetype='application/json'
    )
    return response


def build_valid_json(data):
    """
    Return proper valid json
    """
    response = {"status": "OK"}
    response["data"] = data
    return json.dumps(response)


def build_error_json(error_message):
    """
    Return error json with error message
    """
    response = {"status": "error"}
    response["message"] = error_message
    return json.dumps(response)
