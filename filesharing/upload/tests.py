"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
import doctest
import sys

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}


def load_tests(loader, tests, ignore):
    """
    Load the doctests, otherwise they are not run.

    https://docs.python.org/2/library/doctest.html#unittest-api
    """
    tests.addTests(doctest.DocTestSuite(sys.modules[__name__]))
    return tests
