import time
from services.parser import parse_all_teams, parse_all_players, parse_all_games, parse_boxscores
from db_models import db, Team, Player, Game, Boxscore
from services.utils import get_date, is_date_passed


def create_tables():
    db.create_tables([Team, Player, Game, Boxscore])
    print('tables created')


def insert_all_teams():
    teams = parse_all_teams()
    is_table_empty = not Team.select().exists()
    for team in teams:
        team.save(force_insert=is_table_empty)
    print('teams inserted')


def insert_all_players():
    players = parse_all_players()
    is_table_empty = not Player.select().exists()
    for player in players:
        # if the player doesn't play for any team
        if(player[1] != 0):
            #team = Team.get(Team.id == player[1])
            player[0].team_id = player[1]
            player[0].save(force_insert=is_table_empty)
    print('players inserted')

def are_games_inserted(year, month, day):
    return get_all_games(year=year, month=month, day=day).exists()


'''
    Insert all games in database at given date
'''
def insert_all_games(year, month, day):
    games = parse_all_games(year, month, day)
    should_insert = not are_games_inserted(year=year, month=month, day=day)
    for game in games:
        game.save(force_insert=should_insert)
    print('games inserted')


'''
    Select all games from database at given date
'''
def get_all_games(year, month, day):
    return Game.select().where(Game.date == get_date(year=year, month=month, day=day))


def insert_all_boxscores(year, month, day):
    # check if games have already been inserted and if game date is passed
    if is_date_passed(year=year, month=month, day=day) and not are_games_inserted(year=year, month=month, day=day):
        insert_all_games(year=year, month=month, day=day)
    games = get_all_games(year=year, month=month, day=day)

    for game in games:
        is_game_in_table = not Boxscore.select().where(Boxscore.game == game.id)
        game_boxscores = parse_boxscores(game.id)
        [boxscore.save(force_insert=is_game_in_table)
         for boxscore in game_boxscores]
        time.sleep(1)

    print('boxscores inserted')


def get_ttfl_scores(year, month, day):
    ttfl_scores = Boxscore.select().join(Game).where(Game.date == get_date(
        year=year, month=month, day=day)).order_by(Boxscore.ttfl_score.desc())
    for score in ttfl_scores:
        player = Player.get(Player.id == score.player_id)
        #print(player.name + ' : ' + str(score.ttfl_score))
