from properties.properties import DbProperty
from peewee import Model, CharField, IntegerField, BooleanField, MySQLDatabase, ForeignKeyField, DateField, CompositeKey

db = MySQLDatabase(DbProperty('name'), user=DbProperty('user'),
                   password=DbProperty('pwd'), host=DbProperty('host'), port=DbProperty('port', True))
db.connect()
print("db connected")


class BaseModel(Model):
    class Meta:
        database = db


class Team(BaseModel):
    id = IntegerField(primary_key=True)
    city = CharField()
    name = CharField()
    abbreviation = CharField()
    conference = CharField()
    division = CharField()
    wins = IntegerField()
    losses = IntegerField()


class Player(BaseModel):
    id = IntegerField(primary_key=True)
    team = ForeignKeyField(Team, backref='players', null=True)
    name = CharField()
    has_played_games = BooleanField(default=False)


class Game(BaseModel):
    id = IntegerField(primary_key=True)
    home_team = ForeignKeyField(Team, backref='games')
    visitor_team = ForeignKeyField(Team, backref='games')
    date = DateField()


class Boxscore(BaseModel):
    player = ForeignKeyField(Player, backref='boxscores')
    game = ForeignKeyField(Game, backref='boxscores')
    pts = IntegerField()
    reb = IntegerField()
    ast = IntegerField()
    stl = IntegerField()
    blk = IntegerField()
    to = IntegerField()
    fga = IntegerField()
    fgm = IntegerField()
    fg3a = IntegerField()
    fg3m = IntegerField()
    fta = IntegerField()
    ftm = IntegerField()
    ttfl_score = IntegerField()

    class Meta:
        primary_key = CompositeKey('player', 'game')
        database = db
    # self.ttlf_score = pts + reb + ast + stl + blk - \
    #    to + (fgm-(fga-fgm)) + (fg3m-(fg3a-fg3m)) + (ftm-(fta-ftm))


def create_boxscore(id_player, id_game, pts, reb, ast, stl, blk, to, fga, fgm, fg3a, fg3m, fta, ftm, name):
    ttfl_score = pts + reb + ast + stl + blk - to + \
        (fgm-(fga-fgm)) + (fg3m-(fg3a-fg3m)) + (ftm-(fta-ftm))
    return Boxscore(player_id=id_player,
                    game_id=id_game,
                    pts=pts,
                    reb=reb,
                    ast=ast,
                    stl=stl,
                    blk=blk,
                    to=to,
                    fga=fga,
                    fgm=fgm,
                    fg3a=fg3a,
                    fg3m=fg3m,
                    fta=fta,
                    ftm=ftm,
                    ttfl_score=ttfl_score)
