from flask import Blueprint, url_for, abort, jsonify, Response
from nba_api.stats.endpoints import commonallplayers, commonteamyears, teaminfocommon, commonplayerinfo, scoreboard
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

# boxscoretraditionalv2
@controller.route(api+'/scoreboard/<year>/<month>/<day>')
def getScoreboard(year, month, day):
    response = Response(
        response=parse_all_games(year=year, month=month, day=day),
        status=200,
        mimetype='application/json'
    )
    return response

'''night = parse_all_games(year='2018', month='12', day='9')
for boxscore in night:
    save(boxscore)'''

#parse_all_teams()
