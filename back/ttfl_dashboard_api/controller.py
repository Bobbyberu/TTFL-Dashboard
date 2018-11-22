from flask import Blueprint, url_for, abort, jsonify, Response
from nba_api.stats.endpoints import commonallplayers, commonteamyears, teaminfocommon, commonplayerinfo, scoreboard
from properties.properties import APIProperty
from parser import parse_all_teams, parse_all_players

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
    response = Response(
        response=parse_all_players(),
        status=200,
        mimetype='application/json'
    )
    return response


@controller.route(api + '/player/<id_player>')
def getPlayer(id_player):
    return commonplayerinfo.CommonPlayerInfo(league_id_nullable=APIProperty('LeagueID'), player_id=id_player).get_json()


@controller.route(api+'/allteams')
def allTeams():
    response = Response(
        response=parse_all_teams(),
        status=200,
        mimetype='application/json'
    )
    return response


@controller.route(api+'/team/<id_team>')
def getTeam(id_team):
    return teaminfocommon.TeamInfoCommon(league_id=APIProperty('LeagueID'), team_id=id_team).get_json()


@controller.route(api+'/scoreboard/<year>/<month>/<day>')
def getScoreboard(year, month, day):
    separator = '-'
    game_date = year + separator + month + separator + day
    return scoreboard.Scoreboard(day_offset=0, league_id=APIProperty('LeagueID'), game_date=game_date).get_json();
