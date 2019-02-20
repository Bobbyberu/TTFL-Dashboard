import unittest
import json

from app import create_app_test
from app.db_models import db
from app.services.logger import getLogger
from provisioning import complete_provisioning

URL = '/api/players/'


class TestPlayer(unittest.TestCase):
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


class AllPlayersTestCase(TestPlayer):
    """
    Test getting all players
    """

    def runTest(self):
        r = self.app.get(URL)
        assert r.status_code == 200
        assert len(r.json) == 2
        assert r.json['status'] == 'OK'
        assert len(r.json['data']) == 2
        assert r.json['data'][0] == {'id': 1, 'team': 1, 'first_name': 'Daryl', 'last_name': 'Watkins',
                                     'mpg': 40.9, 'ppg': 20.6, 'rpg': 15.1, 'apg': 2.5, 'spg': 0.5, 'bpg': 3.7}
        assert r.json['data'][1] == {'id': 2, 'team': 1, 'first_name': 'Alexis', 'last_name': 'Ajinça',
                                     'mpg': 32.9, 'ppg': 25.6, 'rpg': 11.1, 'apg': 8.5, 'spg': 1.5, 'bpg': 1.7}


class PlayerByIdTestCase(TestPlayer):
    """
    Test getting player by id
    """

    def runTest(self):
        r = self.app.get(URL + 'id/1')
        assert len(r.json) == 2
        assert r.status_code == 200
        assert r.json['status'] == 'OK'
        assert r.json['data'] == {'id': 1, 'team': 1, 'first_name': 'Daryl', 'last_name': 'Watkins',
                                  'mpg': 40.9, 'ppg': 20.6, 'rpg': 15.1, 'apg': 2.5, 'spg': 0.5, 'bpg': 3.7}


class PlayerByIdNotFoundTestCase(TestPlayer):
    """
    Test if player id doesn't exist
    """

    def runTest(self):
        r = self.app.get(URL + 'id/0')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'No player found'


class PlayerByNameTestCase(TestPlayer):
    """
    Test getting player by name
    """

    def runTest(self):
        r = self.app.get(URL + 'name/alexis')
        assert r.status_code == 200
        assert len(r.json) == 2
        assert r.json['status'] == 'OK'
        assert len(r.json['data']) == 1
        assert r.json['data'][0] == {'id': 2, 'team': 1, 'first_name': 'Alexis', 'last_name': 'Ajinça',
                                     'mpg': 32.9, 'ppg': 25.6, 'rpg': 11.1, 'apg': 8.5, 'spg': 1.5, 'bpg': 1.7}


class PlayerByNameNotFoundTestCase(TestPlayer):
    """
    Test if given name matches with no player
    """

    def runTest(self):
        r = self.app.get(URL + 'name/lebron')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'No player found'


class PlayersByTeamTestCase(TestPlayer):
    """
    Test getting players by teams
    """

    def runTest(self):
        r = self.app.get(URL + 'team/1')
        assert r.status_code == 200
        assert len(r.json) == 2
        assert r.json['status'] == 'OK'
        assert len(r.json['data']) == 2
        assert r.json['data'][0] == {'id': 1, 'team': 1, 'first_name': 'Daryl', 'last_name': 'Watkins',
                                     'mpg': 40.9, 'ppg': 20.6, 'rpg': 15.1, 'apg': 2.5, 'spg': 0.5, 'bpg': 3.7}
        assert r.json['data'][1] == {'id': 2, 'team': 1, 'first_name': 'Alexis', 'last_name': 'Ajinça',
                                     'mpg': 32.9, 'ppg': 25.6, 'rpg': 11.1, 'apg': 8.5, 'spg': 1.5, 'bpg': 1.7}


class PlayersByTeamNotFoundTestCase(TestPlayer):
    """
    Test if team id doesn't exist
    """

    def runTest(self):
        r = self.app.get(URL + 'team/0')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'No team found'


class PlayerTTFLScoresTestCase(TestPlayer):
    """
    Test getting all player's ttfl score
    """

    def runTest(self):
        r = self.app.get(URL + 'ttfl/1/')
        assert r.status_code == 200
        assert len(r.json) == 2
        assert r.json['status'] == 'OK'
        assert len(r.json['data']) == 2
        assert r.json['data'][0] == {
            'ttfl_score': 54, 'date': '2019-02-18 00:00:00'}
        assert r.json['data'][1] == {
            'ttfl_score': 25, 'date': '2019-01-17 00:00:00'}


class PlayerTTFLScoresNotFoundTestCase(TestPlayer):
    """
    Test if player id doesn't exist
    """

    def runTest(self):
        r = self.app.get(URL + 'ttfl/0/')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Player not found'


class PlayerTTFLScoresBetweenDatesTestCase(TestPlayer):
    """
    Test getting all player's ttfl score between given dates
    """

    def runTest(self):
        r = self.app.get(URL + 'ttfl/1/20190120/20190220')
        assert r.status_code == 200
        assert len(r.json) == 2
        assert r.json['status'] == 'OK'
        assert len(r.json['data']) == 1
        assert r.json['data'][0] == {
            'ttfl_score': 54, 'date': '2019-02-18 00:00:00'}


class PlayerTTFLScoresBetweenDatesPlayerNotFoundTestCase(TestPlayer):
    """
    Test getting all player's ttfl score between given dates
    """

    def runTest(self):
        r = self.app.get(URL + 'ttfl/0/20190120/20190220')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Player not found'


class PlayerTTFLScoresInvalidStartDateTestCase(TestPlayer):
    """
    Test getting errors on player's ttfl score between given dates
    """

    def runTest(self):
        # invalid start date
        r = self.app.get(URL + 'ttfl/1/201/20190220')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Invalid date'


class PlayerTTFLScoresInvalidEndDateTestCase(TestPlayer):
    """
    Test getting errors on player's ttfl score between given dates
    """

    def runTest(self):
        # invalid start date
        r = self.app.get(URL + 'ttfl/1/20190101/invalid')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Invalid date'


class PlayerTTFLScoresInvalidTimeIntervalTestCase(TestPlayer):
    """
    Test getting errors on player's ttfl score between given dates
    """

    def runTest(self):
        # invalid start date
        r = self.app.get(URL + 'ttfl/1/20190101/20180101')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Start date is after end date'


class PlayerTTFLScoreAvgTestCase(TestPlayer):
    """
    Test getting player's ttfl avg score average
    """

    def runTest(self):
        r = self.app.get(URL + 'ttfl/avg/1/20190101/20190301')
        assert r.status_code == 200
        assert len(r.json) == 2
        assert r.json['status'] == 'OK'
        assert r.json['data'] == {'player_id': 1, 'first_name': 'Daryl',
                                  'last_name': 'Watkins', 'ttfl_avg': 39.5}


class PlayerTTFLScoresAvgBetweenDatesPlayerNotFoundTestCase(TestPlayer):
    """
    Test getting all player's ttfl avg score between given dates
    """

    def runTest(self):
        r = self.app.get(URL + 'ttfl/avg/0/20190120/20190220')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Could not get average'


class PlayerTTFLScoresAvgInvalidStartDateTestCase(TestPlayer):
    """
    Test getting errors on player's ttfl avg score between given dates
    """

    def runTest(self):
        # invalid start date
        r = self.app.get(URL + 'ttfl/avg/1/201/20190220')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Invalid date'


class PlayerTTFLScoresAvgInvalidEndDateTestCase(TestPlayer):
    """
    Test getting errors on player's ttfl avg score between given dates
    """

    def runTest(self):
        # invalid start date
        r = self.app.get(URL + 'ttfl/avg/1/20190101/invalid')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Invalid date'


class PlayerTTFLScoresAvgInvalidTimeIntervalTestCase(TestPlayer):
    """
    Test getting errors on player's ttfl avg score between given dates
    """

    def runTest(self):
        # invalid start date
        r = self.app.get(URL + 'ttfl/avg/1/20190101/20180101')
        assert r.status_code == 404
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Start date is after end date'


class PlayerAvgStatsTestCase(TestPlayer):
    """
    Test getting player's avg stats
    """

    def runTest(self):
        r = self.app.get(URL + 'avg/1')
        assert r.status_code == 200
        assert len(r.json) == 2
        assert r.json['status'] == 'OK'
        assert r.json['data'] == {'id': 1, 'team': 1, 'first_name': 'Daryl', 'last_name': 'Watkins',
                                  'mpg': 40.9, 'ppg': 20.6, 'rpg': 15.1, 'apg': 2.5,
                                  'spg': 0.5, 'bpg': 3.7, 'avg_ttfl': 39.5}


class PlayerAvgStatsNotFoundTestCase(TestPlayer):
    """
    Test getting error from player's avg stats
    """

    def runTest(self):
        r = self.app.get(URL + 'avg/0')
        assert r.status_code == 400
        assert len(r.json) == 2
        assert r.json['status'] == 'error'
        assert r.json['message'] == 'Could not get average'


def suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [unittest.makeSuite(AllPlayersTestCase, 'all_players'),
         unittest.makeSuite(PlayerByIdTestCase, 'player_by_id'),
         unittest.makeSuite(PlayerByIdNotFoundTestCase,
                            'player_by_id_not_found'),
         unittest.makeSuite(PlayerByNameTestCase, 'player_by_name'),
         unittest.makeSuite(PlayerByNameNotFoundTestCase,
                            'player_by_name_not_found'),
         unittest.makeSuite(PlayersByTeamTestCase, 'players_by_team'),
         unittest.makeSuite(PlayersByTeamNotFoundTestCase,
                            'players_by_team_not_found'),
         unittest.makeSuite(PlayerTTFLScoresTestCase, 'player_all_ttfl_score'),
         unittest.makeSuite(PlayerTTFLScoresNotFoundTestCase,
                            'player_all_ttfl_score_not_found'),
         unittest.makeSuite(PlayerTTFLScoresBetweenDatesTestCase,
                            'player_all_ttfl_score_between_dates'),
         unittest.makeSuite(PlayerTTFLScoresBetweenDatesPlayerNotFoundTestCase,
                            'player_all_ttfl_score_between_dates_player_not_found'),
         unittest.makeSuite(PlayerTTFLScoresInvalidStartDateTestCase,
                            'player_all_ttfl_score_invalid_start_date'),
         unittest.makeSuite(PlayerTTFLScoresInvalidEndDateTestCase,
                            'player_all_ttfl_score_invalid_end_date'),
         unittest.makeSuite(PlayerTTFLScoresInvalidTimeIntervalTestCase,
                            'player_all_ttfl_score_invalid_time_interval'),
         unittest.makeSuite(PlayerTTFLScoreAvgTestCase,
                            'player_all_ttfl_score_avg'),
         unittest.makeSuite(PlayerTTFLScoresAvgBetweenDatesPlayerNotFoundTestCase,
                            'player_all_ttfl_score_avg_between_dates_player_not_found'),
         unittest.makeSuite(PlayerTTFLScoresAvgInvalidStartDateTestCase,
                            'player_all_ttfl_score_avg_invalid_start_date'),
         unittest.makeSuite(PlayerTTFLScoresAvgInvalidEndDateTestCase,
                            'player_all_ttfl_score_avg_invalid_end_date'),
         unittest.makeSuite(PlayerTTFLScoresAvgInvalidTimeIntervalTestCase,
                            'player_all_ttfl_score_avg_invalid_time_interval'),
         unittest.makeSuite(PlayerAvgStatsTestCase, 'player_avg_stats'), ]
    )
    return suite
