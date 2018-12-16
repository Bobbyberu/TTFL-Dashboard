import json
from datetime import datetime
from flask import Blueprint, url_for, abort, jsonify, Response
from db_models import Team, Player, Game, Boxscore
from db_controller import get_all_boxscores
from services.utils import get_json_boxscore_api

api_controller = Blueprint('api_controller', __name__)
api = '/api'


@api_controller.route(api)
def apiFunction():
    abort(404)


@api_controller.route('/test')
def test():
    contents = json.loads(get_json_boxscore_api(2018, 11, 15, 21800213))
    contents = json.dumps(contents['stats']['activePlayers'])

    response = Response(
        response=contents,
        status=200,
        mimetype='application/json'
    )
    return response


@api_controller.route(api+'/teams/')
def get_teams():
    """
    Return all current nba teams
    """
    all_teams = Team.select()
    if all_teams:
        json_response = build_valid_json(
            [team.__dict__['__data__'] for team in all_teams])
        status = 200
    else:
        json_response = build_error_json('No team were found')
        status = 404

    return build_response(json_response, status)


@api_controller.route(api+'/teams/id/<int:id>')
def get_team_by_id(id: int):
    """
    Return team corresponding to given id
    """
    team = Team.select().where(Team.id == id)
    if team:
        json_response = build_valid_json(team.get().__dict__['__data__'])
        status = 200
    else:
        json_response = build_error_json('No team were found')
        status = 404

    return build_response(json_response, status)


@api_controller.route(api+'/players/')
def get_players():
    """
    Return all current nba players
    """
    all_players = Player.select().order_by(Player.name)
    if all_players:
        json_response = build_valid_json(
            [player.__dict__['__data__'] for player in all_players])
        status = 200
    else:
        json_response = build_error_json('No player were found')
        status = 404

    return build_response(json_response, status)


@api_controller.route(api+'/players/id/<int:id>')
def get_player_by_id(id: int):
    """
    Return player corresponding to given id
    """
    player = Player.select().where(Player.id == id)
    if player:
        json_response = build_valid_json(player.get().__dict__['__data__'])
        status = 200
    else:
        json_response = build_error_json('No player found')
        status = 404

    return build_response(json_response, status)


@api_controller.route(api+'/players/name/<name>')
def get_player_by_name(name: str):
    """
    Return a player or a list of players with corresponding name
    """
    players = Player.select().where(Player.name.contains(name))
    if players:
        json_response = build_valid_json(
            [player.__dict__['__data__'] for player in players])
        status = 200
    else:
        json_response = build_error_json('No player found')
        status = 404

    return build_response(json_response, status)

@api_controller.route(api+'/players/team/<int:id>')
def get_team_players(id: int):
    """
    Return all players in given team
    """
    players = Player.select().where(Player.team == id)
    if players:
        json_response = build_valid_json(
            [player.__dict__['__data__'] for player in players])
        status = 200
    else:
        json_response = build_error_json('No team found')
        status = 404

    return build_response(json_response, status)



@api_controller.route(api+'/boxscores/<int:year>/<int:month>/<int:day>')
def get_boxscores(year: int, month: int, day: int):
    """
    Return all boxscores at given date
    """
    try:
        datetime(year, month, day)
    except ValueError:
        json_response = build_error_json('Invalid date')
        return build_response(json_response, 403)

    all_boxscores = get_all_boxscores(year, month, day)
    if all_boxscores:
        json_response = build_valid_json([boxscore.__dict__['__data__']
                                    for boxscore in all_boxscores])
        status = 200
    else:
        json_response = build_error_json(
            'Impossible to get boxscores with a date in the future')
        status = 403

    return build_response(json_response, status)


def build_response(json_response, status):
    """
    Build response object to be returned by api
    """
    return Response(
        response=json_response,
        status=status,
        mimetype='application/json'
    )


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
