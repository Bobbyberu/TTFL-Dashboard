import json
from datetime import datetime
from flask import abort, Blueprint, jsonify, Response, url_for
from sqlalchemy.sql import func
from app.db_models import Boxscore, Game, Player, Team
from app.services.utils import is_date_passed

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
    all_teams = Team.query.all()
    if all_teams:
        json_response = build_valid_json(
            [team.serialize() for team in all_teams])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('No team were found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/teams/id/<int:id>')
def get_team_by_id(id: int):
    """
    Return team corresponding to given id
    """
    team = Team.query.filter_by(_id=id).first()
    if team:
        json_response = build_valid_json(team.serialize())
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('No team were found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/')
def get_players():
    """
    Return all current nba players
    """
    all_players = Player.query.all()
    if all_players:
        json_response = build_valid_json(
            [player.serialize() for player in all_players])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('No player were found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/id/<int:id>')
def get_player_by_id(id: int):
    """
    Return player corresponding to given id
    """
    player = Player.query.filter_by(_id=id).first()
    if player:
        json_response = build_valid_json(player.serialize())
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('No player found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/name/<name>')
def get_player_by_name(name: str):
    """
    Return a player or a list of players with corresponding name
    """
    players = Player.query\
        .filter((Player.first_name.like("%{}%".format(name)))
                | (Player.last_name.like("%{}%".format(name)))).all()
    if players:
        json_response = build_valid_json(
            [player.serialize() for player in players])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('No player found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/team/<int:id>')
def get_team_players(id: int):
    """
    Return all players in given team
    """
    players = Player.query.filter_by(team_id=id).all()
    if players:
        json_response = build_valid_json(
            [player.serialize() for player in players])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('No team found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/ttfl/<int:id>/')
def get_all_ttfl_perfs_player(id: int):
    """
    Return all ttfl score for given player
    """
    perfs = Boxscore.query.filter_by(player_id=id)\
        .join(Boxscore.game).order_by(Game.date.desc()).all()
    if perfs:
        json_response = build_valid_json(
            [{"ttfl_score": perf.ttfl_score, "date": perf.game.date} for perf in perfs])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('Player not found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/ttfl/<int:id>/<start_date>/<end_date>')
def get_perfs_ttfl_between_dates(id, start_date, end_date):
    """
    Return all player ttfl score between given dates
    """
    try:
        start_date = datetime.strptime(start_date, '%Y%m%d')
        end_date = datetime.strptime(end_date, '%Y%m%d')
    except ValueError:
        json_response = build_error_json('Invalid date')
        abort(build_response(json_response, 404))

    if(start_date > end_date):
        json_response = build_error_json('Start date is after end date')
        abort(build_response(json_response, 404))

    perfs = Boxscore.query.filter_by(player_id=id)\
        .join(Boxscore.game).filter(Game.date.between(start_date, end_date)).all()

    if perfs:
        json_response = build_valid_json(
            [{"ttfl_score": perf.ttfl_score, "date": perf.game.date} for perf in perfs])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json('Player not found')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/players/ttfl/avg/<int:id>/<start_date>/<end_date>')
def get_avg_ttfl_player_between_dates(id, start_date, end_date):
    """
    Return average player ttfl score between given dates
    """
    try:
        start_date = datetime.strptime(start_date, '%Y%m%d')
        end_date = datetime.strptime(end_date, '%Y%m%d')
    except ValueError:
        json_response = build_error_json('Invalid date')
        abort(build_response(json_response, 404))

    if(start_date > end_date):
        json_response = build_error_json('Start date is after end date')
        abort(build_response(json_response, 404))

    query = Boxscore.query.filter_by(player_id=id).\
        join(Boxscore.game).\
        filter(Game.date.between(start_date, end_date)).\
        with_entities(Boxscore, func.avg(
            Boxscore.ttfl_score).label('ttfl_avg')).first()

    if query[0] and query[1]:
        # selecting first element
        boxscore = query[0]
        json_response = build_valid_json(
            {'player_id': boxscore.player_id, 'first_name': boxscore.player.first_name,
             'last_name': boxscore.player.last_name, 'ttfl_avg': query[1]})
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
    query_avg_ttfl = Boxscore.query.filter_by(player_id=id)\
        .with_entities(func.avg(
            Boxscore.ttfl_score).label('ttfl_avg')).first()

    player = Player.query.filter_by(_id=id).first()

    if player and query_avg_ttfl:
        response = player.serialize()
        # selecting first element as ttfl average
        response['avg_ttfl'] = query_avg_ttfl[0]

        json_response = build_valid_json(response)
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
        date = datetime(year, month, day)
    except ValueError:
        json_response = build_error_json('Invalid date')
        abort(build_response(json_response, 404))

    if not is_date_passed(year, month, day):
        json_response = build_error_json('Date in the future')
        abort(build_response(json_response, 404))

    boxscores = Boxscore.query\
        .join(Boxscore.game)\
        .filter(Game.date == date).order_by(Boxscore.ttfl_score.desc())

    if boxscores:
        json_response = build_valid_json(
            [boxscore.serialize(include_player=True) for boxscore in boxscores])
        return build_response(json_response, 200)


@api_controller.route(api+'/boxscores/player/<int:player>')
def get_player_boxscores(player):
    """
    Return all given player boxscores
    """
    boxscores = Boxscore.query.filter_by(player_id=player).all()
    if boxscores:
        json_response = build_valid_json(
            [boxscore.serialize() for boxscore in boxscores])
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

    if not is_date_passed(year, month, day):
        json_response = build_error_json('Date in the future')
        abort(build_response(json_response, 404))

    boxscore = Boxscore.query.filter_by(player_id=player)\
        .join(Boxscore.game)\
        .filter(Game.date == date).first()
    if boxscore:
        json_response = build_valid_json(boxscore.serialize())
        return build_response(json_response, 200)
    else:
        json_response = build_error_json(
            'Could not get boxscore')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/boxscores/topttfl')
def get_top_ttfl():
    results = Boxscore.query\
        .with_entities(Boxscore, func.avg(Boxscore.ttfl_score).label('ttfl_avg'))\
        .group_by(Boxscore.player_id)\
        .order_by(func.avg(Boxscore.ttfl_score).desc())\
        .limit(20)
    if results:
        json_response = build_valid_json(
            [{"player_id": result[0].player._id, "ttfl_score": result.ttfl_avg,
              "first_name": result[0].player.first_name, "last_name": result[0].player.last_name} for result in results])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json(
            'Could not get players')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/boxscores/topttfl/<int:year>/<int:month>/<int:day>')
def get_top_ttfl_given_date(year, month, day):
    """
    Return best 20 ttfl performances at given date
    """
    try:
        date = datetime(year, month, day)
    except ValueError:
        json_response = build_error_json('Invalid date')
        abort(build_response(json_response, 404))

    if not is_date_passed(year, month, day):
        json_response = build_error_json('Date in the future')
        abort(build_response(json_response, 404))

    boxscores = Boxscore.query.join(Boxscore.game)\
        .filter(Game.date == date)\
        .order_by(Boxscore.ttfl_score.desc())\
        .limit(20)
    if boxscores:
        json_response = build_valid_json(
            [{"player_id": boxscore.player_id, "ttfl_score": boxscore.ttfl_score,
              "first_name": boxscore.player.first_name, "last_name": boxscore.player.last_name} for boxscore in boxscores])
        return build_response(json_response, 200)
    else:
        json_response = build_error_json(
            'Could not get boxscores')
        abort(build_response(json_response, 404))


@api_controller.route(api+'/boxscores/allttfl/<int:year>/<int:month>/<int:day>')
def get_ttfl_night_scores(year, month, day):
    """
    Return all ttfl performance at one given night
    """
    try:
        date = datetime(year, month, day)
    except ValueError:
        json_response = build_error_json('Invalid date')
        abort(build_response(json_response, 404))

    if not is_date_passed(year, month, day):
        json_response = build_error_json('Date in the future')
        abort(build_response(json_response, 404))

    boxscores = Boxscore.query.join(Boxscore.game)\
        .filter(Game.date == date)\
        .order_by(Boxscore.ttfl_score.desc())
    if boxscores:
        json_response = build_valid_json(
            [{"player_id": boxscore.player_id, "ttfl_score": boxscore.ttfl_score,
                "first_name": boxscore.player.first_name, "last_name": boxscore.player.last_name} for boxscore in boxscores])
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
