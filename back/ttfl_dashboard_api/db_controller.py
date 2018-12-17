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
    [team.save(force_insert=is_table_empty) for team in teams]
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
    return get_all_games(year, month, day).exists()


def insert_all_games(year: int, month: int, day: int):
    """
    Insert all games in database at given date
    """
    games = parse_all_games(year, month, day)
    should_insert = not get_all_games(year, month, day)
    [game.save(force_insert=should_insert) for game in games]
    print('games inserted')


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
    # check if games have already been inserted and if game date is passed
    if is_date_passed(year, month, day) and not get_all_games(year, month, day):
        insert_all_games(year, month, day)
    games = get_all_games(year, month, day)
    for game in games:
        is_game_in_table = not Boxscore.select().where(Boxscore.game == game).exists()
        game_boxscores = parse_boxscores(year, month, day, game)
        [boxscore.save(force_insert=is_game_in_table)
         for boxscore in game_boxscores]

    print('boxscores inserted')


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


def get_ttfl_scores(year: int, month: int, day: int):
    """
    Get ttfl scores at a given date, ordered by most points
    """
    ttfl_scores = Boxscore.select().join(Game).where(Game.date == datetime(
        year, month, day)).order_by(Boxscore.ttfl_score.desc())
    for score in ttfl_scores:
        player = Player.get(Player.id == score.player_id)
        #print(player.name + ' : ' + str(score.ttfl_score))


def initialize_database(year: int, month: int, day: int):
    """
    Function called at server first start, to create all tables and get data at given date
    """
    create_tables()
    # insert_all_teams()
    #insert_all_players()
    insert_all_boxscores(year, month, day)


def test():
    player = get_player_by_id(2544)
    print(player.__dict__['__data__'])
    #[print(boxscore) for boxscore in boxscores]
