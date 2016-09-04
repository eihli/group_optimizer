import unittest
import shutil
import os
import time
import csv
from ..arrangement_formatter import ArrangementFormatter

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
            csv_file = ArrangementFormatter.create_csv_from_groups(self.groups, f)
            self.assertTrue(hasattr(csv_file, 'read'), "Expected csv to be an instance of file but it doesnt' have the 'read' method.")

        with open(self.tmp_dir + '/output.csv', 'r') as f:
            csv_reader = csv.reader(f)
            first_line = next(csv_reader)
            self.assertEqual(first_line, ['Group 0:', '', '0: a', '3: d'])

            second_line = next(csv_reader)
            self.assertEqual(second_line, ['Group 1:', '', '1: b', '4: e'])

