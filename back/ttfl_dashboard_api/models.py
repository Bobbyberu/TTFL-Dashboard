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
