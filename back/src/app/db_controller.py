from datetime import datetime, timedelta
from app.db_models import db, Team, Player, Game, Boxscore
from app.properties.properties import APIProperty
from app.services.logger import getLogger
from app.services.parser import parse_all_teams, parse_all_players, parse_all_games, parse_boxscores
from app.services.utils import is_date_passed

logger = getLogger(__name__)


def create_tables():
    """
    Create all tables in database
    """
    logger.info('Creating tables...')
    db.create_tables([Team, Player, Game, Boxscore])
    logger.info('Tables created')


def insert_all_teams():
    """
    Insert all current nba teams in database
    """
    logger.info('Inserting teams...')
    teams = parse_all_teams()
    is_table_empty = not Team.select().exists()
    [team.save(force_insert=is_table_empty) for team in teams]
    logger.info('Teams inserted')


def insert_all_players():
    """
    Insert all players currently playing in the league in database
    """
    logger.info('Inserting players...')
    players = parse_all_players()
    is_table_empty = not Player.select().exists()
    for player in players:
        player.save(force_insert=is_table_empty)
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
    should_insert = not get_all_games(year, month, day)
    [game.save(force_insert=should_insert) for game in games]
    logger.info(date_to_string(year, month, day) + ' games inserted')


def get_all_games(year: int, month: int, day: int):
    """
    Select all games from database at given date
    """
    games = Game.select().where(Game.date == datetime(year, month, day))
    return [game.id for game in games]


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
        is_game_in_table = not Boxscore.select().where(Boxscore.game == game).exists()
        game_boxscores = parse_boxscores(year, month, day, game)
        [boxscore.save(force_insert=is_game_in_table)
         for boxscore in game_boxscores]

    logger.info('%s boxscores inserted', date_to_string(year, month, day))


def get_all_boxscores(year: int, month: int, day: int):
    """
    Return all boxscores at given date
    """
    if(not is_date_passed(year, month, day)):
        return None

    games = get_all_games(year, month, day)
    boxscores = Boxscore.select().where(
        Boxscore.game.in_(games)).order_by(Boxscore.ttfl_score.desc())
    return boxscores


def season_catch_up():
    """
    insert all games and boxscores since beginning of the season
    """
    season_debut_year = int(APIProperty('season_debut_year'))
    season_debut_month = int(APIProperty('season_debut_month'))
    season_debut_day = int(APIProperty('season_debut_day'))
    season_debut_date = datetime(
        season_debut_year, season_debut_month, season_debut_day)

    # get number of day passed since season start
    day_passed = int((datetime.now() - season_debut_date).days)

    for i in range(day_passed):
        #season_debut_date + timedelta(i)
        current_date = season_debut_date + timedelta(i)
        insert_all_boxscores(
            current_date.year, current_date.month, current_date.day)


def initialize_database():
    """
    Function called at server first start, to create all tables and get data at given date
    """
    create_tables()
    insert_all_teams()
    insert_all_players()
    season_catch_up()


def date_to_string(year, month, day):
    """
    format date in order to be displayed for logging
    """
    separator = '/'
    return str(day) + separator + str(month) + separator + str(year)


def test():
    test = Boxscore.select().where(Boxscore.player == 2544).dicts()

    print([print(row) for row in test])