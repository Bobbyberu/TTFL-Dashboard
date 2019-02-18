import unittest
import json

from app import create_app_test
from app.db_models import db
from app.services.logger import getLogger
from provisioning import provisioning_team

URL = '/api/teams/'


class TestTeam(unittest.TestCase):
    def setUp(self):
        app = create_app_test()
        self.app = app

        db.init_app(app)
        db.app = app
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            provisioning_team(db)
        self.app = app.test_client()


class AllTeamsTestCase(TestTeam):
    """
    Test getting all teams
    """

    def runTest(self):
        r = self.app.get(URL)
        assert len(r.json) == 2
        assert r.status_code == 200
        assert r.json['status'] == 'OK'
        assert len(r.json['data']) == 2
        assert r.json['data'][0] == {'id': 1, 'name': 'ASVEL', 'city': 'Villeurbanne',
                                     'abbreviation': 'AVL', 'conference': 'conference', 'division': 'division', 'W': 99, 'L': 0}

        assert r.json['data'][1] == {'id': 2, 'name': 'Beaujolais', 'city': 'Quncié',
                                     'abbreviation': 'BB', 'conference': 'conference', 'division': 'division', 'W': 0, 'L': 99}


class TeamByIdTestCase(TestTeam):
    """
    Test getting one team by id
    """

    def runTest(self):
        r = self.app.get(URL + 'id/1')
        assert len(r.json) == 2
        assert r.status_code == 200
        assert r.json['status'] == 'OK'
        assert r.json['data'] == {'id': 1, 'name': 'ASVEL', 'city': 'Villeurbanne',
                                  'abbreviation': 'AVL', 'conference': 'conference', 'division': 'division', 'W': 99, 'L': 0}


class TeamByIdNotFoundTestCase(TestTeam):
    """
    Test if team doesn't exist
    """

    def runTest(self):
        r = self.app.get(URL + 'id/999')
        assert r.status_code == 404
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'No team were found'


def suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [unittest.makeSuite(AllTeamsTestCase, 'all_teams'),
         unittest.makeSuite(TeamByIdTestCase, 'team_by_id'),
         unittest.makeSuite(TeamByIdNotFoundTestCase, 'team_by_id_not_found')]
    )
    return suite
