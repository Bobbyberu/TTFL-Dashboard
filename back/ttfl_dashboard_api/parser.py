import json
import time
from nba_api.stats.endpoints import commonallplayers, commonteamyears, teaminfocommon, commonplayerinfo, scoreboard
from properties.properties import APIProperty
from models import Team, Player

######## COMMON FUNCTIONS ########


def get_result_set(raw_json, header_name=None):
    # headers contains the name of each field the API returns
    result_sets_raw = raw_json['resultSets']

    # some endpoints might have several headers
    if header_name is not None:
        for i in range(len(result_sets_raw)):
            if result_sets_raw[i]['name'] == header_name:
                result_set = result_sets_raw[i]
                break
    else:
        # if not, just pick the first one
        result_set = result_sets_raw[0]

    # build dict to get headers and their position to facilitate data retrieving
    headers = {}
    for i in range(len(result_set['headers'])):
        headers[result_set['headers'][i]] = i

    return headers, result_set['rowSet']


def get_ids(headers, id_field, data):
    indexes = []
    index_id = headers[id_field]
    for i in range(len(data)):
        indexes.append(data[i][index_id])
    return indexes
################

# parsing for teams #


def parse_all_teams():
    all_teams_raw = json.loads(commonteamyears.CommonTeamYears(
        APIProperty('LeagueID')).get_json())
    headers, row_set = get_result_set(all_teams_raw)

    # retrieving each team id
    teams_id = get_ids(headers, 'TEAM_ID', row_set)
    teams = []
    for team_id in teams_id:
        teams = parse_team(team_id, teams)

    return json.dumps(teams)


def parse_team(id_team, teams):
    # if too much requests sent, nba_api block you for a little amoiht of time
    time.sleep(1)
    raw_team = json.loads(teaminfocommon.TeamInfoCommon(
        league_id=APIProperty('LeagueID'), team_id=id_team).get_json())
    headers, row_set = get_result_set(raw_team, "TeamInfoCommon")
    if row_set:
        # only the first row_set contains player information
        data = row_set[0]
        team = Team(data[headers['TEAM_ID']], data[headers['TEAM_CITY']], data[headers['TEAM_NAME']], data[headers['TEAM_ABBREVIATION']],
                    data[headers['TEAM_CONFERENCE']], data[headers['TEAM_DIVISION']], data[headers['W']], data[headers['L']]).__dict__
        print(team)
        teams.append(team)
    return teams
#                       #

# parsing for players #


def parse_all_players():
    all_players_raw = json.loads(commonallplayers.CommonAllPlayers(
        is_only_current_season='1', league_id=APIProperty('LeagueID'), season=APIProperty('CurrentSeason')).get_json())
    headers, row_set = get_result_set(all_players_raw)

    players = []
    for player in row_set:
        players = parse_player(headers, player, players)
    
    return json.dumps(players)


def parse_player(headers, player_array, players):
    has_played_games = False
    if(player_array[headers['GAMES_PLAYED_FLAG']] == 'Y'):
        has_played_games = True
    player = Player(player_array[headers['PERSON_ID']], player_array[headers['TEAM_ID']], player_array[headers['DISPLAY_FIRST_LAST']],
        has_played_games)
    players.append(player.__dict__)
    return players

#                       #
