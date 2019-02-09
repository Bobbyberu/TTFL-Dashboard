import json
import time
from datetime import datetime
from nba_api.stats.endpoints import commonallplayers, commonteamyears, teaminfocommon, commonplayerinfo, scoreboard, boxscoretraditionalv2, playercareerstats
from app.properties.properties import APIProperty
from app.db_models import Team, Player, Game, Boxscore
from app.services.utils import format_game_id, format_stat
from dateutil.parser import parse
from app.services.http_endpoints import get_all_players_json, get_player_json, get_all_games, get_json_boxscore_api
from app.services.logger import getLogger

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
    player_json = get_player_json(player['personId'])
    if player_json is not None:
        raw_player = json.loads(player_json)

        # get first league in case player has been playing in several league (like standard, africa, vegas...)
        league_key = list(raw_player['league'])[0]
        player_stats = raw_player['league'][league_key]['stats']['latest']
        logger.info('creating {} {}'.format(
            player['firstName'], player['lastName']))
        player = Player(id=player['personId'], first_name=player['firstName'], last_name=player['lastName'],
                        team=player['teamId'], mpg=player_stats['mpg'], ppg=player_stats['ppg'],
                        rpg=player_stats['rpg'], apg=player_stats['apg'], spg=player_stats['spg'], bpg=player_stats['bpg'])
        return player


def parse_common_player_info(player_id: str):
    """
    Parse player info from CommonPlayerInfo endpoint (when player has not been insert in database)
    """
    player_json = json.loads(
        commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_json())
    headers_player, row_set_player = get_result_set(
        player_json, 'CommonPlayerInfo')

    if row_set_player:
        data_player = row_set_player[0]

        # check if player has a team
        if data_player[headers_player['TEAM_ID']]:
            team = int(data_player[headers_player['TEAM_ID']])
        else:
            team = None

        player = {'personId': data_player[headers_player['PERSON_ID']], 'firstName': data_player[headers_player['FIRST_NAME']],
                  'lastName': data_player[headers_player['LAST_NAME']], 'teamId': team}

        parsed_player = parse_player(player)
        if parsed_player is not None:
            return parsed_player
        else:
            # in case player is not registered by data.nba.net api
            stats_json = json.loads(playercareerstats.PlayerCareerStats(
                player_id=player_id, per_mode36='PerGame', league_id_nullable=APIProperty('LeagueID')).get_json())
            headers_stats, row_set_stats = get_result_set(
                stats_json, 'SeasonTotalsRegularSeason')

            # get stats for current season
            data_stats = row_set_stats[-1]
            return Player(id=data_player[headers_player['PERSON_ID']], first_name=data_player[headers_player['FIRST_NAME']],
                            last_name=data_player[headers_player['LAST_NAME']], team=team,
                            mpg=data_stats[headers_stats['MIN']], ppg=data_stats[headers_stats['MIN']],
                            rpg=data_stats[headers_stats['REB']], apg=data_stats[headers_stats['AST']],
                            spg=data_stats[headers_stats['STL']], bpg=data_stats[headers_stats['BLK']])
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
                player = parse_common_player_info(
                    boxscore['personId'])
                if player is not None:
                    player.save(force_insert=True)

            perf = Boxscore(player_id=format_stat(boxscore['personId']), game_id=game_id, dnp=dnp, min=boxscore['min'],
                            pts=format_stat(boxscore['points']),
                            reb=format_stat(boxscore['totReb']),
                            ast=format_stat(boxscore['assists']),
                            stl=format_stat(boxscore['steals']),
                            blk=format_stat(boxscore['blocks']),
                            to=format_stat(boxscore['turnovers']),
                            fga=format_stat(boxscore['fga']),
                            fgm=format_stat(boxscore['fgm']),
                            tpa=format_stat(boxscore['tpa']),
                            tpm=format_stat(boxscore['tpm']),
                            fta=format_stat(boxscore['fta']),
                            ftm=format_stat(boxscore['ftm']))
            all_game_perfs.append(perf)
    return all_game_perfs


def is_game_live(game_stats_json):
    """
    Return True if game is ongoing
    """
    basic_game_data = game_stats_json['basicGameData']
    return basic_game_data['isGameActivated']
#                       #
