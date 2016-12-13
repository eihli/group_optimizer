import unittest
import time
import os
import shutil
import csv
from tempfile import TemporaryFile
from group_optimizer.grouper import CategoryGrouper
from group_optimizer.grouper import Group
from group_optimizer.arrangement_formatter import ArrangementFormatter

class CategoryPreferenceTestCase(unittest.TestCase):
    """Test grouping individuals by categorical preference

    Given categories as columns and individuals as rows with
    each cell ranking the individuals preference.
    """

    def setUp(self):
        csv = [
            ['', 'React', 'Angular'],
            ['Alice', '2', '1'],
            ['Bob', '1', '2'],
            ['Mallory', '1', '2'],
            ['Chance', '2', '1']
            ]
        self.csv_str = '\n'.join([','.join(row) for row in csv])
        self.individuals = ArrangementFormatter.survey_to_dict(self.csv_str)

    def test_group(self):
        expected_groups = [[0, 3], [1, 2]]
        groups = CategoryGrouper.group(self.individuals, 2)
        #self.assertEqual(groups, expected_groups)

    def test_score_group(self):
        score = CategoryGrouper.score_group(self.individuals, [0, 2], ['React', 'Angular'])
        self.assertEqual(score, 1)
