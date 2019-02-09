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


def format_stat(stat):
    """
    Parse stat to int or return 0 if stat is unsepcified
    """
    if not stat:
        return 0
    return int(stat)
