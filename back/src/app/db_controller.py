from datetime import datetime, timedelta
from app.db_models import db, Boxscore, Game, Player, Team
from app.properties.properties import APIProperty
from app.services.logger import getLogger
from app.services.parser import parse_all_teams, parse_all_players, parse_all_games, parse_boxscores
from app.services.utils import is_date_passed

logger = getLogger(__name__)


def insert_all_teams():
    """
    Insert all current nba teams in database
    """
    logger.info('Inserting teams...')
    teams = parse_all_teams()
    [db.session.merge(team) for team in teams]
    db.session.commit()
    logger.info('Teams inserted')


def insert_all_players():
    """
    Insert all players currently playing in the league in database
    """
    logger.info('Inserting players...')
    players = parse_all_players()
    [db.session.merge(player) for player in players]
    db.session.commit()
    logger.info('Players inserted')


def are_games_inserted(year: int, month: int, day: int):
    """
    Check if games at given date have already been inserted in database
    """
    return get_all_games(year, month, day).exists()


def insert_all_games(year: int, month: int, day: int):
    """
    Insert all games in database at given date
    """
    logger.info('Inserting %s games...', date_to_string(year, month, day))
    games = parse_all_games(year, month, day)
    [db.session.add(game) for game in games]
    db.session.commit()
    logger.info(date_to_string(year, month, day) + ' games inserted')


def get_all_games(year: int, month: int, day: int):
    """
    Select all games from database at given date
    """
    return Game.query.filter_by(date=datetime(year, month, day)).all()


def insert_all_boxscores(year: int, month: int, day: int):
    """
    Insert all players stats in database at given date
    """
    logger.info('Inserting %s boxscores...', date_to_string(year, month, day))
    # check if games have already been inserted and if game date is passed
    if is_date_passed(year, month, day) and not get_all_games(year, month, day):
        insert_all_games(year, month, day)
    games = get_all_games(year, month, day)
    for game in games:
        game_boxscores = parse_boxscores(year, month, day, game)
        [db.session.merge(boxscore) for boxscore in game_boxscores]
        db.session.commit()

    logger.info('%s boxscores inserted', date_to_string(year, month, day))


def season_catch_up():
    """
    insert all games and boxscores since beginning of the season
    """
    season_debut_year = int(APIProperty('season_debut_year'))
    season_debut_month = int(APIProperty('season_debut_month'))
    season_debut_day = int(APIProperty('season_debut_day'))
    season_debut_date = datetime(
        season_debut_year, season_debut_month, season_debut_day)

    # get all star weekend dates in order to ignore games played at these dates
    all_star_debut, all_star_end = get_all_star_weekend_dates()

    # get number of day passed since season start
    day_passed = int((datetime.now() - season_debut_date).days)

    for i in range(day_passed):
        current_date = season_debut_date + timedelta(i)

        if not all_star_debut <= current_date <= all_star_end:
            insert_all_boxscores(
                current_date.year, current_date.month, current_date.day)


def populate_database():
    """
    Function called at server first start, to create all tables and get data at given date
    """
    insert_all_teams()
    insert_all_players()
    season_catch_up()


def date_to_string(year, month, day):
    """
    format date in order to be displayed for logging
    """
    separator = '/'
    return str(day) + separator + str(month) + separator + str(year)


def get_all_star_weekend_dates():
    all_star_debut = datetime(int(APIProperty('all_star_debut_year')),
                              int(APIProperty('all_star_debut_month')),
                              int(APIProperty('all_star_debut_day')))

    all_star_end = datetime(int(APIProperty('all_star_end_year')),
                            int(APIProperty('all_star_end_month')),
                            int(APIProperty('all_star_end_day')))

    return all_star_debut, all_star_end
