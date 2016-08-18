import unittest
from ..grouper import Grouper

class GroupitTestCase(unittest.TestCase):
    def setUp(self):
        self.grouper = Grouper()

    def test_groupit_exists(self):
        self.assertIsInstance(self.grouper, Grouper)
