from app import create_app
from app.db_models import db, Boxscore, Game, Player, Team
import datetime


def complete_provisioning(db):
    provisioning_team(db)
    provisioning_player(db)
    provisioning_game(db)
    provisioning_boxscore(db)


def provisioning_team(db):
    """
    Add teams in sqlite test db
    """
    t1 = Team(id=1, city='Villeurbanne', name='ASVEL', abbreviation='AVL',
              conference='conference', division='division', wins=99, losses=0)
    t2 = Team(id=2, city='Quncié', name='Beaujolais', abbreviation='BB',
              conference='conference', division='division', wins=0, losses=99)
    db.session.add(t1)
    db.session.add(t2)
    db.session.commit()


def provisioning_player(db):
    """
    Add players in sqlite test db
    """
    p1 = Player(id=1, team_id=1, first_name='Daryl', last_name='Watkins',
                mpg=40.9, ppg=20.6, rpg=15.1, apg=2.5, spg=0.5, bpg=3.7)
    p2 = Player(id=2, team_id=1, first_name='Alexis', last_name='Ajinça',
                mpg=32.9, ppg=25.6, rpg=11.1, apg=8.5, spg=1.5, bpg=1.7)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()


def provisioning_game(db):
    """
    Add games in sqlite test db
    """
    g1 = Game(1, 1, 2, datetime.date(2019, 2, 18), True)
    g2 = Game(2, 1, 2, datetime.date(2019, 1, 17), False)
    db.session.add(g1)
    db.session.add(g2)
    db.session.commit()


def provisioning_boxscore(db):
    """
    Add boxscores in sqlite test db
    """
    b1 = Boxscore(1, 1, False, '12:34', 21, 10, 15, 1, 3, 0, 10, 7, 2, 2, 4, 1)
    b2 = Boxscore(2, 1, False, '22:45', 0, 0, 0, 0, 0, 2, 10, 0, 2, 0, 4, 0)
    b3 = Boxscore(1, 2, False, '48:00', 4, 0, 18, 2, 0, 4, 16, 7, 3, 2, 8, 7)
    db.session.add(b1)
    db.session.add(b2)
    db.session.add(b3)
    db.session.commit()
