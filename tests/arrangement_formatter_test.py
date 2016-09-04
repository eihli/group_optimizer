import unittest
import shutil
import os
import time
from ..arrangement_formatter import ArrangementFormatter
from ..participant import Participant

class ArrangementFormatterTest(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = 'tmp' + str(time.time())
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        self.groups = [
            [
                {'affinities': [5], 'interpersonal_refusals': [], 'id': 0, 'technical_refusals': [3], 'name': 'a'},
                {'affinities': [2], 'interpersonal_refusals': [], 'id': 3, 'technical_refusals': [0], 'name': 'd'}],
            [
                {'affinities': [], 'interpersonal_refusals': [], 'id': 1, 'technical_refusals': [], 'name': 'b'},
                {'affinities': [], 'interpersonal_refusals': [], 'id': 4, 'technical_refusals': [], 'name': 'e'}],
            [
                {'affinities': [], 'interpersonal_refusals': [5], 'id': 2, 'technical_refusals': [], 'name': 'c'},
                {'affinities': [], 'interpersonal_refusals': [], 'id': 5, 'technical_refusals': [2], 'name': 'f'}
            ]
        ]

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_export_groups_to_csv(self):
        with open(self.tmp_dir + '/output.csv', 'w') as f:
            csv = ArrangementFormatter.create_csv_from_groups(self.groups, f)
            self.assertTrue(hasattr(csv, 'read'), "Expected csv to be an instance of file but it doesnt' have the 'read' method.")

