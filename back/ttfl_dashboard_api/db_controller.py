import time
from datetime import datetime
from services.parser import parse_all_teams, parse_all_players, parse_all_games, parse_boxscores
from db_models import db, Team, Player, Game, Boxscore
from services.utils import is_date_passed


def create_tables():
    """
    Create all tables in database
    """
    db.create_tables([Team, Player, Game, Boxscore])
    print('tables created')


def insert_all_teams():
    """
    Insert all current nba teams in database
    """
    teams = parse_all_teams()
    is_table_empty = not Team.select().exists()
    for team in teams:
        team.save(force_insert=is_table_empty)
    print('teams inserted')


def insert_all_players():
    """
    Insert all players currently playing in the league in database
    """
    players = parse_all_players()
    is_table_empty = not Player.select().exists()
    for player in players:
        # if the player doesn't play for any team
        if(player[1] != 0):
            #team = Team.get(Team.id == player[1])
            player[0].team_id = player[1]
            player[0].save(force_insert=is_table_empty)
    print('players inserted')


def are_games_inserted(year: int, month: int, day: int):
    """
    Check if games at given date have already been inserted in database
    """
    return get_all_games(year=year, month=month, day=day).exists()


def insert_all_games(year: int, month: int, day: int):
    """
    Insert all games in database at given date
    """
    games = parse_all_games(year, month, day)
    should_insert = not are_games_inserted(year=year, month=month, day=day)
    for game in games:
        game.save(force_insert=should_insert)
    print('games inserted')


def get_all_games(year: int, month: int, day: int):
    """
    Select all games from database at given date
    """
    games = Game.select().where(Game.date == datetime(year=year, month=month, day=day))
    return [game.id for game in games]


def insert_all_boxscores(year: int, month: int, day: int):
    """
    Insert all players stats in database at given date
    """
    # check if games have already been inserted and if game date is passed
    if is_date_passed(year=year, month=month, day=day) and not are_games_inserted(year=year, month=month, day=day):
        insert_all_games(year=year, month=month, day=day)
    games = get_all_games(year=year, month=month, day=day)

    for game in games:
        is_game_in_table = not Boxscore.select().where(Boxscore.game == game.id).exists()
        game_boxscores = parse_boxscores(game.id)
        [boxscore.save(force_insert=is_game_in_table)
         for boxscore in game_boxscores]
        time.sleep(1)

    print('boxscores inserted')


def get_all_boxscores(year: int, month: int, day: int):
    """
    Return all boxscores at given date
    """
    if(not is_date_passed(year, month, day)):
        return None

    games = get_all_games(year=year, month=month, day=day)
    boxscores = Boxscore.select().where(Boxscore.game in games).order_by(Boxscore.ttfl_score.desc())
    return boxscores


def get_ttfl_scores(year: int, month: int, day: int):
    """
    Get ttfl scores at a given date, ordered by most points
    """
    ttfl_scores = Boxscore.select().join(Game).where(Game.date == datetime(
        year=year, month=month, day=day)).order_by(Boxscore.ttfl_score.desc())
    for score in ttfl_scores:
        player = Player.get(Player.id == score.player_id)
        #print(player.name + ' : ' + str(score.ttfl_score))


def initialize_database(year: int, month: int, day: int):
    """
    Function called at server first start, to create all tables and get data at given date
    """
    create_tables()
    insert_all_teams()
    insert_all_players()
    insert_all_boxscores(year, month, day)

def test():
    games = Game.select()
    print([game.id for game in games])
    #[print(boxscore) for boxscore in boxscores]