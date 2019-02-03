import json
import time
from datetime import datetime
from nba_api.stats.endpoints import commonallplayers, commonteamyears, teaminfocommon, commonplayerinfo, scoreboard, boxscoretraditionalv2
from properties.properties import APIProperty
from db_models import Team, Player, Game, Boxscore, create_boxscore
from services.utils import format_game_id, format_stat
from dateutil.parser import parse
from services.http_endpoints import get_all_players_json, get_player_json, get_all_games, get_json_boxscore_api
from services.logger import getLogger

logger = getLogger(__name__)


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
        logger.info('creating {}'.format(data[headers['TEAM_NAME']]))
        team = Team(id=int(data[headers['TEAM_ID']]), city=data[headers['TEAM_CITY']], name=data[headers['TEAM_NAME']], abbreviation=data[headers['TEAM_ABBREVIATION']],
                    conference=data[headers['TEAM_CONFERENCE']], division=data[headers['TEAM_DIVISION']], wins=int(data[headers['W']]), losses=int(data[headers['L']]))
        teams.append(team)
    return teams
#                       #


# parsing for players #
def parse_all_players():
    """
    Parse all players information
    """
    raw_players = json.loads(get_all_players_json())
    all_players = raw_players['league']['standard']
    all_player_parsed = []
    for player in all_players:
        all_player_parsed.append(parse_player(player))
    return all_player_parsed


def parse_player(player):
    """
    Parse player information and create player databas object
    """
    raw_player = json.loads(get_player_json(player['personId']))
    league_key = ''

    # check if player has a team
    if player['teamId']:
        team = int(player['teamId'])
    else:
        team = None

    # get first league in case player has been playing in several league (like standard, africa, vegas...)
    league_key = list(raw_player['league'])[0]
    player_stats = raw_player['league'][league_key]['stats']['latest']
    logger.info('creating {} {}'.format(
        player['firstName'], player['lastName']))
    player = Player(id=player['personId'], first_name=player['firstName'], last_name=player['lastName'],
                    team=team, mpg=player_stats['mpg'], ppg=player_stats['ppg'],
                    rpg=player_stats['rpg'], apg=player_stats['apg'], spg=player_stats['spg'], bpg=player_stats['bpg'])
    return player


def parse_common_player_info(player_id: str):
    """
    Parse player info from CommonPlayerInfo endpoint (when player has not been insert in database)
    """
    player_json = json.loads(
        commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_json())
    headers, row_set = get_result_set(player_json, 'CommonPlayerInfo')

    if row_set:
        data = row_set[0]

        player = {'personId': data[headers['PERSON_ID']], 'firstName': data[headers['FIRST_NAME']],
                  'lastName': data[headers['LAST_NAME']], 'teamId': data[headers['TEAM_ID']]}
        return parse_player(player)
    else:
        return None


#                       #


# parsing for games #
def parse_all_games(year, month, day):
    raw_games = json.loads(get_all_games(year, month, day))
    all_games = raw_games['games']

    parsed_games = []
    for game in all_games:
        home_team = game['hTeam']
        visitor_team = game['vTeam']
        game_date = datetime.strptime(game['startDateEastern'], '%Y%m%d')
        parsed_game = Game(id=game['gameId'], home_team=home_team['teamId'],
                           visitor_team=visitor_team['teamId'], date=game_date)
        parsed_games.append(parsed_game)
    return parsed_games

#                       #


# parsing for boxscore #
def parse_boxscores(year, month, day, game_id):
    """
    Get and parse all players stats at one given game
    """
    all_game_perfs = []
    game_stats = json.loads(get_json_boxscore_api(year, month, day, game_id))

    # Change game live status if it's ongoing
    query_game_live = Game.update(is_game_live=is_game_live(
        game_stats)).where(Game.id == game_id)
    query_game_live.execute()
    game_start_UTC = parse(
        game_stats['basicGameData']['startTimeUTC']).replace(tzinfo=None)
    # do not parse the boxscore if game has not started yet
    if datetime.utcnow() >= game_start_UTC:
        player_stats = game_stats['stats']['activePlayers']
        for boxscore in player_stats:
            # check if the player has played the game
            dnp = False
            if boxscore['dnp']:
                dnp = True

            # if player is not in database, insert it
            if not Player.select().where(Player.id == format_stat(boxscore['personId'])):
                parse_common_player_info(
                    boxscore['personId']).save(force_insert=True)

            perf = create_boxscore(format_stat(boxscore['personId']), game_id, dnp, boxscore['min'],
                                   format_stat(boxscore['points']),
                                   format_stat(boxscore['totReb']),
                                   format_stat(boxscore['assists']),
                                   format_stat(boxscore['steals']),
                                   format_stat(boxscore['blocks']),
                                   format_stat(boxscore['turnovers']),
                                   format_stat(boxscore['fga']),
                                   format_stat(boxscore['fgm']),
                                   format_stat(boxscore['tpa']),
                                   format_stat(boxscore['tpm']),
                                   format_stat(boxscore['fta']),
                                   format_stat(boxscore['ftm']))
            all_game_perfs.append(perf)
    return all_game_perfs


def is_game_live(game_stats_json):
    """
    Return True if game is ongoing
    """
    basic_game_data = game_stats_json['basicGameData']
    return basic_game_data['isGameActivated']
#                       #
