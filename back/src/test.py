import unittest
from unit_test import test_team


def suite():
    """
    All unit tests which must be executed
    """
    suite = unittest.TestSuite()
    suite.addTest(test_team.suite())
    return suite


if __name__ == '__main__':
    """
    Will launch all app unit tests
    """
    unittest.main(defaultTest='suite')
