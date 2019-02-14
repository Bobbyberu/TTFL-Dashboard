from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Team(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    city = db.Column(db.String(50))
    name = db.Column(db.String(50))
    abbreviation = db.Column(db.String(50))
    conference = db.Column(db.String(50))
    division = db.Column(db.String(50))
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)

    def __repr__(self):
        return '<Team %r>' % self.name

    def serialize(self):
        return {'id': self._id, 'name': self.name, 'city': self.city,
                'abbreviation': self.abbreviation, 'conference': self.conference,
                'division': self.division, 'W': self.wins, 'L': self.losses}


class Player(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, ForeignKey('team.id'), nullable=True)
    team = db.relationship('Team', backref='players')
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    mpg = db.Column(db.Float)
    ppg = db.Column(db.Float)
    rpg = db.Column(db.Float)
    apg = db.Column(db.Float)
    spg = db.Column(db.Float)
    bpg = db.Column(db.Float)

    def __init__(self, id, team_id, first_name, last_name, mpg, ppg, rpg, apg, spg, bpg):
        self._id = id
        self.team_id = team_id
        self.first_name = first_name
        self.last_name = last_name
        self.mpg = mpg
        self.ppg = ppg
        self.rpg = rpg
        self.apg = apg
        self.spg = spg
        self.bpg = bpg

    def serialize(self, short=False):
        if short is True:
            return {'id': self._id, 'team': self.team_id, 'first_name': self.first_name,
                    'last_name': self.last_name}
        else:
            return {'id': self._id, 'team': self.team_id, 'first_name': self.first_name,
                    'last_name': self.last_name, 'mpg': self.mpg, 'ppg': self.ppg,
                    'rpg': self.rpg, 'apg': self.apg, 'spg': self.spg, 'bpg': self.bpg}


class Game(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    home_team_id = db.Column(db.Integer, ForeignKey('team.id'))
    home_team = relationship('Team', foreign_keys=[home_team_id])
    visitor_team_id = db.Column(db.Integer, ForeignKey('team.id'))
    visitor_team = db.relationship('Team', foreign_keys=[visitor_team_id])
    date = db.Column(db.DateTime)
    is_game_live = db.Column(db.Boolean, default=False)

    def __init__(self, id, home_team_id, visitor_team_id, date, is_game_live):
        self._id = id
        self.home_team_id = home_team_id
        self.visitor_team_id = visitor_team_id
        self.date = date
        self.is_game_live = is_game_live


class Boxscore(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, ForeignKey('player.id'))
    player = relationship('Player')
    game_id = db.Column(db.Integer, ForeignKey('game.id'))
    game = relationship('Game')
    min = db.Column(db.String(50), default='0:00')
    dnp = db.Column(db.Boolean, default=False)
    pts = db.Column(db.Integer)
    reb = db.Column(db.Integer)
    ast = db.Column(db.Integer)
    stl = db.Column(db.Integer)
    blk = db.Column(db.Integer)
    to = db.Column(db.Integer)
    fga = db.Column(db.Integer)
    fgm = db.Column(db.Integer)
    tpa = db.Column(db.Integer)
    tpm = db.Column(db.Integer)
    fta = db.Column(db.Integer)
    ftm = db.Column(db.Integer)
    ttfl_score = db.Column(db.Integer)

    def __init__(self, player_id, game_id, dnp, min, pts, reb, ast, stl, blk, to, fga, fgm, tpa, tpm, fta, ftm):
        self.player_id = player_id
        self.game_id = game_id
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
        super(Boxscore, self).__init__()

    def serialize(self, include_player=False):
        if include_player is True:
            return {'player': self.player.serialize(short=True), 'game': self.game_id, 'min': self.min, 'dnp': self.dnp, 'pts': self.pts,
                    'reb': self.reb, 'ast': self.ast, 'stl': self.stl, 'blk': self.blk, 'to': self.to, 'fga': self.fga,
                    'fgm': self.fgm, 'tpa': self.tpa, 'tpm': self.tpm, 'fta': self.fta, 'ftm': self.ftm, 'ttfl_score': self.ttfl_score}
        else:
            return {'player': self.player_id, 'game': self.game_id, 'min': self.min, 'dnp': self.dnp, 'pts': self.pts,
                    'reb': self.reb, 'ast': self.ast, 'stl': self.stl, 'blk': self.blk, 'to': self.to, 'fga': self.fga,
                    'fgm': self.fgm, 'tpa': self.tpa, 'tpm': self.tpm, 'fta': self.fta, 'ftm': self.ftm, 'ttfl_score': self.ttfl_score}
