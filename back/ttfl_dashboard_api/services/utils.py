from datetime import datetime
from urllib import request


def get_date(year, month, day):
    return datetime(year, month, day)


def format_game_id(game_id: str) -> str:
    """
    Return an id correctly formatted
    Ids should always be 10 digits
    If it is shorter it adds 0 before the string

    "2" becomes "0000000002"
    "1548" becomes "0000001548"
    """
    return game_id.strip().zfill(10)


def is_date_passed(year, month, day):
    return datetime(year=year, month=month, day=day) <= datetime.now()

def build_url_boxscores(year: int, month: int, day: int, game_id: int) -> str:
    """
    Build proper data.nba.net url to be called to retrieve live boxscores
    """
    base = 'https://data.nba.net/prod/v1/'
    end = '_boxscore.json'
    date = str(year) + str(month).zfill(2) + str(day).zfill(2)
    return base + date + '/' + format_game_id(str(game_id)) + end

def get_json_boxscore_api(year, month, day, game_id):
    return request.urlopen(build_url_boxscores(year, month, day, game_id)).read()


def format_stat(stat):
    """
    Parse stat to int or return 0 if stat is unsepcified
    """
    if not stat:
        return 0
    return int(stat)