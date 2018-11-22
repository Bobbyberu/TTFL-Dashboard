class Team:
    def __init__(self, id, city, name, abbreviation, conference, division, wins, losses):
        self.id = id
        self.city = city
        self.name = name
        self.abbreviation = abbreviation
        self.conference = conference
        self.division = division
        self.wins = wins
        self.losses = losses


class Player:
    def __init__(self, id, id_team, name, has_played_games):
        self.id = id
        self.id_team = id_team
        self.name = name
        self.has_played_games = has_played_games


class Boxscore:
    def __init__(self, id_player, id_game, pts, reb, ast, stl, blk, to, fga, fgm, fg3a, fg3m, fta, ftm, name):
        self.id_player = id_player
        self.id_game = id_game
        self.pts = pts
        self.reb = reb
        self.ast = ast
        self.stl = stl
        self.blk = blk
        self.to = to
        self.fga = fga
        self.fgm = fgm
        self.fg3a = fg3a
        self.fg3m = fg3m
        self.fta = fta
        self.ftm = ftm
        self.name = name
        self.ttlf_score = pts + reb + ast + stl + blk - \
            to + (fgm-(fga-fgm)) + (fg3m-(fg3a-fg3m)) + (ftm-(fta-ftm))
