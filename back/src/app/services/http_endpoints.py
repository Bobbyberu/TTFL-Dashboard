from app.services.utils import format_game_id
from urllib import request


def get_json_boxscore_api(year: int, month: int, day: int, game_id: int) -> str:
    """
    Build proper data.nba.net url to be called to retrieve live boxscores
    """
    base = 'https://data.nba.net/prod/v1/'
    end = '_boxscore.json'
    date = str(year) + str(month).zfill(2) + str(day).zfill(2)
    url = base + date + '/' + format_game_id(str(game_id)) + end
    return request.urlopen(url).read()


def get_all_players_json():
    """
    Retrieve json with all players currently active in the nba
    """
    return request.urlopen('http://data.nba.net/prod/v1/2018/players.json').read()


def get_player_json(player_id):
    """
    Retrieve player detailed information
    """
    url = 'http://data.nba.net/prod/v1/2018/players/{}_profile.json'.format(
        player_id)
    return request.urlopen(url).read()


def get_all_games(year, month, day):
    """
    Return all games at given date
    """
    date = '{}{}{}'.format(year, str(month).zfill(2), str(day).zfill(2))
    url = 'http://data.nba.net/prod/v1/{}/scoreboard.json'.format(date)
    return request.urlopen(url).read()
