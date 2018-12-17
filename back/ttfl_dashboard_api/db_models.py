from properties.properties import DbProperty
from peewee import Model, CharField, IntegerField, BooleanField, MySQLDatabase, ForeignKeyField, DateField, CompositeKey

# connection to database
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
    is_game_live = BooleanField(default=False)


class Boxscore(BaseModel):
    player = ForeignKeyField(Player, backref='boxscores')
    game = ForeignKeyField(Game, backref='boxscores')
    min = CharField(default='0:00')
    dnp = BooleanField()
    pts = IntegerField()
    reb = IntegerField()
    ast = IntegerField()
    stl = IntegerField()
    blk = IntegerField()
    to = IntegerField()
    fga = IntegerField()
    fgm = IntegerField()
    tpa = IntegerField()
    tpm = IntegerField()
    fta = IntegerField()
    ftm = IntegerField()
    ttfl_score = IntegerField()

    class Meta:
        primary_key = CompositeKey('player', 'game')
        database = db


def create_boxscore(player_id, game_id, dnp, min, pts, reb, ast, stl, blk, to, fga, fgm, tpa, tpm, fta, ftm):
    # calculate ttfl score from player's stats
    ttfl_score = pts + reb + ast + stl + blk - to + \
        (fgm-(fga-fgm)) + (tpm-(tpa-tpm)) + (ftm-(fta-ftm))
    boxscore = Boxscore(player_id=player_id,
                        game_id=game_id,
                        dnp=dnp,
                        pts=pts,
                        reb=reb,
                        ast=ast,
                        stl=stl,
                        blk=blk,
                        to=to,
                        fga=fga,
                        fgm=fgm,
                        tpa=tpa,
                        tpm=tpm,
                        fta=fta,
                        ftm=ftm,
                        ttfl_score=ttfl_score)
    # set field only if it exists
    if min:
        boxscore.min = min

    return boxscore
