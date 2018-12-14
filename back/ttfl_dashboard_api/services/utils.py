import time
import re
from datetime import datetime, date
from dateutil.parser import parse


def string_to_date(date):
    return parse(date)


def get_date(year, month, day):
    return datetime(year, month, day)


'''
    game_id must be 10 digits
'''
def format_game_id(game_id):
    regex = re.compile('^\d{10}$')
    if not regex.match(game_id):
        for i in range(10-len(game_id)):
            game_id = '0' + game_id
    return game_id


def is_date_passed(year, month, day):
    return get_date(year=year, month=month, day=day) <= datetime.now()