from flask import Blueprint, url_for, abort
from nba_api.stats.endpoints import commonallplayers, commonteamyears, teaminfocommon
from properties.properties import APIProperty

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
    return commonallplayers.CommonAllPlayers('1', APIProperty('LeagueID'), APIProperty('CurrentSeason')).get_json()

@controller.route(api+'/allteams')
def allTeams():
    return commonteamyears.CommonTeamYears(APIProperty('LeagueID')).get_json()

@controller.route(api+'/team/<id_team>')
def getTeam(id_team):
    return teaminfocommon.TeamInfoCommon(league_id=APIProperty('LeagueID'), team_id=id_team).get_json()