import json
from datetime import datetime
from flask import abort, Blueprint, jsonify, Response, url_for
from peewee import fn
from app.db_models import Boxscore, Game, Player, Team
from app.db_controller import get_all_boxscores

api_controller = Blueprint('api_controller', __name__)
api = '/api'


@api_controller.route(api)
def apiFunction():
    abort(404)


@api_controller.route(api+'/teams/')
def get_teams():
    """
    Return all current nba teams
    """
    all_teams = Team.select().dicts()
    if all_teams:
        json_response = build_valid_json(
            [team for team in all_teams])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('No team were found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/teams/id/<int:id>')
def get_team_by_id(id: int):
    """
    Return team corresponding to given id
    """
    team = Team.select().where(Team.id == id)
    if team:
        json_response = build_valid_json(team.get().__dict__['__data__'])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('No team were found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/')
def get_players():
    """
    Return all current nba players
    """
    all_players = Player.select().order_by(Player.last_name).dicts()
    if all_players:
        json_response = build_valid_json(
            [player for player in all_players])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('No player were found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/id/<int:id>')
def get_player_by_id(id: int):
    """
    Return player corresponding to given id
    """
    player = Player.select().where(Player.id == id)
    if player:
        json_response = build_valid_json(player.get().__dict__['__data__'])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('No player found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/name/<name>')
def get_player_by_name(name: str):
    """
    Return a player or a list of players with corresponding name
    """
    players = Player.select().where((Player.first_name.contains(name))
                                    | (Player.last_name.contains(name))).dicts()
    if players:
        json_response = build_valid_json(
            [player for player in players])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('No player found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/team/<int:id>')
def get_team_players(id: int):
    """
    Return all players in given team
    """
    players = Player.select().where(Player.team == id).dicts()
    if players:
        json_response = build_valid_json(
            [player for player in players])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('No team found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/ttfl/<int:id>/')
def get_all_ttfl_perfs_player(id: int):
    """
    Return all ttfl score for given player
    """
    perfs = Boxscore.select(Boxscore.ttfl_score, Game.date).join(
        Game).where(Boxscore.player == id).order_by(Game.date.desc()).dicts()
    if perfs:
        json_response = build_valid_json(
            [perf for perf in perfs])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('Player not found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/ttfl/<int:id>/<start_date>/<end_date>')
def get_perfs_ttfl_between_dates(id, start_date, end_date):
    """
    Return all player ttfl score between given dates
    """
    start_date = datetime.strptime(start_date, '%Y%m%d')
    end_date = datetime.strptime(end_date, '%Y%m%d')

    perfs = Boxscore.select(Boxscore.ttfl_score, Game.date).join(Game).where((Boxscore.player == id) & (
        Game.date.between(start_date, end_date))).order_by(Game.date.desc()).dicts()
    if perfs:
        json_response = build_valid_json(
            [perf for perf in perfs])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('Player not found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/ttfl/avg/<int:id>/<start_date>/<end_date>')
def get_avg_ttfl_player_between_dates(id, start_date, end_date):
    """
    Return average player ttfl score between given dates
    """
    ttfl_avg = Boxscore.select(Boxscore.player, fn.AVG(Boxscore.ttfl_score).alias(
        'ttfl_avg')).join(Game).where((Boxscore.player == id) & (Game.date.between(start_date, end_date))).dicts()

    if ttfl_avg:
        # selecting first element
        json_response = build_valid_json(ttfl_avg[0])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json(
            'Could not get average')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/avg/<int:id>')
def get_player_avg_stats(id: int):
    """
    Return player average stats (minutes, points, rebounds, assists, steal, blocks, ttfl_score)
    """
    player = Boxscore.select(Player.last_name, Player.first_name, Player.mpg, Player.ppg, Player.rpg, Player.apg, Player.spg,
                             Player.bpg, fn.AVG(Boxscore.ttfl_score).alias('ttflpg')).where(Boxscore.player == id).join(Player).dicts()

    if player:
        # selecting first element
        json_response = build_valid_json(player[0])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json(
            'Could not get average')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/boxscores/<int:year>/<int:month>/<int:day>')
def get_boxscores(year: int, month: int, day: int):
    """
    Return all boxscores at given date
    """
    try:
        datetime(year, month, day)
    except ValueError:
        json_response = build_error_json('Invalid date')
        abort(build_response(json_response, 404))

    all_boxscores = get_all_boxscores(year, month, day).dicts()
    if all_boxscores:
        json_response = build_valid_json(
            [boxscore for boxscore in all_boxscores])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json(
            'Impossible to get boxscores with a date in the future')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/boxscores/player/<int:player>')
def get_player_boxscores(player):
    """
    Return all given player boxscores
    """
    boxscores = Boxscore.select().where(Boxscore.player == player).dicts()
    if boxscores:
        json_response = build_valid_json([boxscore for boxscore in boxscores])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json(
            'Could not get boxscores')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/boxscores/player/<int:player>/<int:year>/<int:month>/<int:day>')
def get_player_night_boxscore(player, year, month, day):
    """
    Return player's boxscore at given date
    """
    try:
        date = datetime(year, month, day)
    except ValueError:
        json_response = build_error_json('Invalid date')
        abort(build_response(json_response, 404))

    boxscore = Boxscore.select().join(Game).where(
        (Boxscore.player == player) & (Game.date == date)).get()
    if boxscore:
        json_response = build_valid_json(boxscore.__dict__['__data__'])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json(
            'Could not get boxscores')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/boxscores/topttfl/<int:year>/<int:month>/<int:day>')
def get_top_ttfl(year, month, day):
    """
    Return best 20 ttfl performances at given date
    """
    try:
        date = datetime(year, month, day)
    except ValueError:
        json_response = build_error_json('Invalid date')
        abort(build_response(json_response, 404))

    boxscores = Boxscore.select(Boxscore.ttfl_score, Player.id, Player.first_name, Player.last_name).join(Game).switch(Boxscore).join(Player).where(
        Game.date == date).order_by(Boxscore.ttfl_score.desc()).limit(20).dicts()
    if boxscores:
        json_response = build_valid_json([boxscore for boxscore in boxscores])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json(
            'Could not get boxscores')
        abort(build_response(json_response, 404))


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

    # default = str to help format date
    return json.dumps(response, default=str)


def build_error_json(error_message):
    """
    Return error json with error message
    """
    response = {"status": "error"}
    response["message"] = error_message
    return json.dumps(response)
