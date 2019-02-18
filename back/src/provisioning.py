from app import create_app
from app.db_models import db, Boxscore, Game, Player, Team


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
