from peewee import Model, CharField, IntegerField, BooleanField, MySQLDatabase, ForeignKeyField, DateField, CompositeKey, FloatField
from app.properties.properties import DbProperty

# connection to database
db = MySQLDatabase(DbProperty('name'), user=DbProperty('user'),
                   password=DbProperty('pwd'), host=DbProperty('host'), port=DbProperty('port', True))
db.connect()


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
    first_name = CharField()
    last_name = CharField()
    mpg = FloatField()
    ppg = FloatField()
    rpg = FloatField()
    apg = FloatField()
    spg = FloatField()
    bpg = FloatField()


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

    def __init__(self, player_id, game_id, dnp, min, pts, reb, ast, stl, blk, to, fga, fgm, tpa, tpm, fta, ftm):
        super(Boxscore, self).__init__()
        self.player = player_id
        self.game = game_id
        self.min = min
        self.dnp = dnp
        self.pts = pts
        self.reb = reb
        self.ast = ast
        self.stl = stl
        self.blk = blk
        self.to = to
        self.fga = fga
        self.fgm = fgm
        self.tpa = tpa
        self.tpm = tpm
        self.fta = fta
        self.ftm = ftm
        self.ttfl_score = pts + reb + ast + stl + blk - to + \
            (fgm-(fga-fgm)) + (tpm-(tpa-tpm)) + (ftm-(fta-ftm))
