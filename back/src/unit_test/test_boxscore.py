import unittest
import json

from app import create_app_test
from app.db_models import db
from app.services.logger import getLogger
from provisioning import complete_provisioning

URL = '/api/boxscores/'


class TestBoxscore(unittest.TestCase):
    def setUp(self):
        app = create_app_test()
        self.app = app

        db.init_app(app)
        db.app = app
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            complete_provisioning(db)
        self.app = app.test_client()


class AllBoxscoresTestCase(TestBoxscore):
    """
    Test getting all boxscores at given date
    """

    def runTest(self):
        r = self.app.get(URL + '2019/2/18')
        assert r.status_code == 200
        assert len(r.json) == 2
        assert r.json['status'] == 'OK'
        assert len(r.json['data']) == 2
        assert r.json['data'][0] == {'player': {'id': 1, 'team': 1, 'first_name': 'Daryl', 'last_name': 'Watkins'}, 'game': 1,
                                     'min': '12:34', 'dnp': False, 'pts': 21, 'reb': 10, 'ast': 15, 'stl': 1, 'blk': 3, 'to': 0,
                                     'fga': 10, 'fgm': 7, 'tpa': 2, 'tpm': 2, 'fta': 4, 'ftm': 1, 'ttfl_score': 54}
        assert r.json['data'][1] == {'player': {'id': 2, 'team': 1, 'first_name': 'Alexis', 'last_name': 'Ajinça'}, 'game': 1,
                                     'min': '22:45', 'dnp': False, 'pts': 0, 'reb': 0, 'ast': 0, 'stl': 0, 'blk': 0, 'to': 2,
                                     'fga': 10, 'fgm': 0, 'tpa': 2, 'tpm': 0, 'fta': 4, 'ftm': 0, 'ttfl_score': -18}


class AllBoxscoresInvalidDateTestCase(TestBoxscore):
    """
    Test getting boxscores with invalid date
    """

    def runTest(self):
        r = self.app.get(URL + '2019/32/18')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Invalid date'


class AllBoxscoresDateFutureTestCase(TestBoxscore):
    """
    Test getting boxscores with date in the future
    """

    def runTest(self):
        r = self.app.get(URL + '9999/2/18')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Date in the future'


class AllPlayerBoxscoresTestCase(TestBoxscore):
    """
    Test getting all player's boxscores
    """

    def runTest(self):
        r = self.app.get(URL + 'player/1')
        assert r.status_code == 200
        assert len(r.json) == 2
        assert r.json['status'] == 'OK'
        assert len(r.json['data']) == 2
        assert r.json['data'][0] == {'player': 1, 'game': 1, 'min': '12:34', 'dnp': False, 'pts': 21, 'reb': 10, 'ast': 15, 'stl': 1,
                                     'blk': 3, 'to': 0, 'fga': 10, 'fgm': 7, 'tpa': 2, 'tpm': 2, 'fta': 4, 'ftm': 1, 'ttfl_score': 54}
        assert r.json['data'][1] == {'player': 1, 'game': 2, 'min': '48:00', 'dnp': False, 'pts': 4, 'reb': 0, 'ast': 18, 'stl': 2,
                                     'blk': 0, 'to': 4, 'fga': 16, 'fgm': 7, 'tpa': 3, 'tpm': 2, 'fta': 8, 'ftm': 7, 'ttfl_score': 25}


class AllPlayerBoxscoresNotFoundTestCase(TestBoxscore):
    """
    Test getting unknown player's boxscores
    """

    def runTest(self):
        r = self.app.get(URL + 'player/0')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Could not get boxscores'


class PlayerNightBoxscoreTestCase(TestBoxscore):
    """
    Test getting player boxscore at given date
    """

    def runTest(self):
        r = self.app.get(URL + 'player/1/2019/2/18')
        assert r.status_code == 200
        assert len(r.json) == 2
        assert r.json['status'] == 'OK'
        assert r.json['data'] == {'player': 1, 'game': 1, 'min': '12:34', 'dnp': False, 'pts': 21, 'reb': 10, 'ast': 15, 'stl': 1,
                                  'blk': 3, 'to': 0, 'fga': 10, 'fgm': 7, 'tpa': 2, 'tpm': 2, 'fta': 4, 'ftm': 1, 'ttfl_score': 54}


class PlayerNightBoxscoreInvalidDateTestCase(TestBoxscore):
    """
    Test getting player night boxscore with invalid date
    """

    def runTest(self):
        r = self.app.get(URL + 'player/1/2019/32/18')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Invalid date'


class PlayerNightBoxscoreDateFutureTestCase(TestBoxscore):
    """
    Test getting player night boxscore with date in the future
    """

    def runTest(self):
        r = self.app.get(URL + 'player/1/9999/2/18')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Date in the future'


class PlayerNightBoxscoreNotFoundTestCase(TestBoxscore):
    """
    Test getting unknown player's night boxscore
    """

    def runTest(self):
        r = self.app.get(URL + 'player/0/2019/2/18')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Could not get boxscore'


class TopTTFLTestCase(TestBoxscore):
    """
    Test getting top ttfl scores at given date
    """

    def runTest(self):
        r = self.app.get(URL + 'topttfl/2019/2/18')
        assert r.status_code == 200
        assert len(r.json) == 2
        assert r.json['status'] == 'OK'
        assert len(r.json['data']) == 2
        assert r.json['data'][0] == {
            'ttfl_score': 54, 'player_id': 1, 'first_name': 'Daryl', 'last_name': 'Watkins'}
        assert r.json['data'][1] == {
            'ttfl_score': -18, 'player_id': 2, 'first_name': 'Alexis', 'last_name': 'Ajinça'}


class TopTTFLInvalidDateTestCase(TestBoxscore):
    """
    Test getting top ttfl scores with invalid date
    """

    def runTest(self):
        r = self.app.get(URL + 'topttfl/2019/32/18')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Invalid date'


class TopTTFLDateFutureTestCase(TestBoxscore):
    """
    Test getting top ttfl scores with date in the future
    """

    def runTest(self):
        r = self.app.get(URL + 'topttfl/9999/2/18')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Date in the future'


def suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [unittest.makeSuite(AllBoxscoresTestCase, 'all_boxscores'),
         unittest.makeSuite(AllBoxscoresInvalidDateTestCase,
                            'all_boxscores_invalid_date'),
         unittest.makeSuite(AllBoxscoresDateFutureTestCase,
                            'all_boxscores_date_future'),
         unittest.makeSuite(AllPlayerBoxscoresTestCase,
                            'all_player_boxscores'),
         unittest.makeSuite(AllPlayerBoxscoresNotFoundTestCase,
                            'all_player_boxscores_not_found'),
         unittest.makeSuite(PlayerNightBoxscoreTestCase,
                            'player_night_boxscore'),
         unittest.makeSuite(PlayerNightBoxscoreInvalidDateTestCase,
                            'player_night_boxscore_invalid_date'),
         unittest.makeSuite(PlayerNightBoxscoreDateFutureTestCase,
                            'player_night_boxscore_date_future'),
         unittest.makeSuite(PlayerNightBoxscoreNotFoundTestCase,
                            'player_night_boxscore_not_found'),
         unittest.makeSuite(TopTTFLTestCase, 'top_ttfl'),
         unittest.makeSuite(TopTTFLInvalidDateTestCase,
                            'top_ttfl_invalid_date'),
         unittest.makeSuite(TopTTFLDateFutureTestCase, 'top_ttfl_date_future')]
    )
    return suite
