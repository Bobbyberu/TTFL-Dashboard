import json
import time
from nba_api.stats.endpoints import commonallplayers, commonteamyears, teaminfocommon, commonplayerinfo, scoreboard, boxscoretraditionalv2
from properties.properties import APIProperty
from db_models import Team, Player, Game, Boxscore, create_boxscore
from services.utils import format_game_id
from dateutil.parser import parse

######## COMMON FUNCTIONS ########


def get_result_set(raw_json: str, header_name=None):
    """
    Get data from a certain header from NBA API
    """
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
    """
    Get only IDs from row_set
    """
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

    # return json.dumps(teams)
    return teams


def parse_team(id_team, teams):
    # if too much requests sent, nba_api block you for a little amoiht of time
    time.sleep(1)
    raw_team = json.loads(teaminfocommon.TeamInfoCommon(
        league_id=APIProperty('LeagueID'), team_id=id_team).get_json())
    headers, row_set = get_result_set(raw_team, "TeamInfoCommon")
    if row_set:
        # only the first row_set contains player information
        data = row_set[0]
        team = Team(id=int(data[headers['TEAM_ID']]), city=data[headers['TEAM_CITY']], name=data[headers['TEAM_NAME']], abbreviation=data[headers['TEAM_ABBREVIATION']],
                    conference=data[headers['TEAM_CONFERENCE']], division=data[headers['TEAM_DIVISION']], wins=int(data[headers['W']]), losses=int(data[headers['L']]))
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

    return players


def parse_player(headers, player_array, players):
    """
    Will return a tuple (player, team_id) to help build the foreign key
    """
    has_played_games = False
    if(player_array[headers['GAMES_PLAYED_FLAG']] == 'Y'):
        has_played_games = True
    player = (Player(id=player_array[headers['PERSON_ID']], name=player_array[headers['DISPLAY_FIRST_LAST']],
                     has_played_games=has_played_games), player_array[headers['TEAM_ID']])
    players.append(player)
    return players

#                       #


# parsing for boxscore #
def parse_all_games(year, month, day):
    separator = '-'
    game_date = str(year) + separator + str(month) + separator + str(day)
    raw_games = json.loads(scoreboard.Scoreboard(
        day_offset=0, league_id=APIProperty('LeagueID'), game_date=game_date).get_json())
    headers, row_set = get_result_set(
        raw_json=raw_games, header_name='GameHeader')
    games = []
    for game in row_set:
        parsed_game = Game(id=game[headers['GAME_ID']], home_team=game[headers['HOME_TEAM_ID']],
                           visitor_team=game[headers['VISITOR_TEAM_ID']], date=parse(game[headers['GAME_DATE_EST']]))
        games.append(parsed_game)
    return games


def parse_boxscores(game_id):
    """
    Get and parse all players stats at one given game
    """
    all_game_perfs = []
    raw_boxscore = json.loads(boxscoretraditionalv2.BoxScoreTraditionalV2(
        end_period=1, end_range=0, game_id=format_game_id(str(game_id)), range_type=0, start_period=1, start_range=0).get_json())
    headers, row_set = get_result_set(
        raw_json=raw_boxscore, header_name='PlayerStats')
    for game_perf in row_set:
        # check that the player has played during the game
        if not game_perf[headers['COMMENT']]:
            perf = create_boxscore(game_perf[headers['PLAYER_ID']], game_perf[headers['GAME_ID']], game_perf[headers['PTS']], game_perf[headers['REB']], game_perf[headers['AST']], game_perf[headers['STL']], game_perf[headers['BLK']],
                                   game_perf[headers['TO']], game_perf[headers['FGA']], game_perf[headers['FGM']], game_perf[headers['FG3A']], game_perf[headers['FG3M']], game_perf[headers['FTA']], game_perf[headers['FTM']], game_perf[headers['PLAYER_NAME']])
            all_game_perfs.append(perf)
    return all_game_perfs
#                       #
