import unittest
import shutil
import os
import time
import csv
from functools import reduce
from group_optimizer.arrangement_formatter import ArrangementFormatter

class ArrangementFormatterTest(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = 'tmp' + str(time.time())
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        self.arrangement = [
            {
                'id': 0,
                'name': 'a',
                'technical_refusals': [3],
                'interpersonal_refusals': [],
                'affinities': [5]
            },
            {
                'id': 1,
                'name': 'b',
                'technical_refusals': [],
                'interpersonal_refusals': [],
                'affinities': []
            },
            {
                'id': 2,
                'name': 'c',
                'technical_refusals': [],
                'interpersonal_refusals': [5],
                'affinities': []
            },
            {
                'id': 3,
                'name': 'd',
                'technical_refusals': [0],
                'interpersonal_refusals': [],
                'affinities': [2]
            },
            {
                'id': 4,
                'name': 'e',
                'technical_refusals': [],
                'interpersonal_refusals': [],
                'affinities': []
            },
            {
                'id': 5,
                'name': 'f',
                'technical_refusals': [2],
                'interpersonal_refusals': [],
                'affinities': []
            }
        ]

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

    def test_create_arrangement_from_csv(self):
        with open(self.tmp_dir + '/input.csv', 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['', 'a', 'b', 'c'])
            csv_writer.writerow(['a', '', '1', '-1'])
            csv_writer.writerow(['b', '1', '', '-1'])
            csv_writer.writerow(['c', '', '', ''])

        with open(self.tmp_dir + '/input.csv', 'r') as f:
            arrangement = ArrangementFormatter.create_arrangement_from_csv(f)
            participant = reduce(lambda x, p: p if p['id'] == 0 and x == None else x, arrangement, None)

            self.assertEqual(participant['name'], 'a')
            self.assertEqual(participant['technical_refusals'], [2])
            self.assertEqual(participant['affinities'], [1])

            participant = reduce(lambda x, p: p if p['id'] == 1 and x == None else x, arrangement, None)
            self.assertEqual(participant['name'], 'b')
            self.assertEqual(participant['affinities'], [0])

    def test_create_csv_from_groups(self):
        with open(self.tmp_dir + '/output.csv', 'w') as f:
            csv_file = ArrangementFormatter.create_csv_from_groups(self.groups, f)
            self.assertTrue(hasattr(csv_file, 'read'), "Expected csv to be an instance of file but it doesnt' have the 'read' method.")

        with open(self.tmp_dir + '/output.csv', 'r') as f:
            csv_reader = csv.reader(f)
            first_line = next(csv_reader)
            self.assertEqual(first_line, ['Group 0:', 'Happiness Score: -200', '0: a', '3: d'])

            second_line = next(csv_reader)
            self.assertEqual(second_line, ['', '0: a', '', '-1'])

            third_line = next(csv_reader)
            self.assertEqual(third_line, ['', '3: d', '-1', ''])

            fourth_line = next(csv_reader)
            self.assertEqual(fourth_line, ['Group 1:', 'Happiness Score: 0', '1: b', '4: e'])

            fifth_line = next(csv_reader)
            self.assertEqual(fifth_line, ['', '1: b', '', ''])

    def test_survey_to_dict(self):
        survey = ',React,Angular\na,1,0\nb,0,1'
        result = ArrangementFormatter.survey_to_dict(survey)
        self.assertEqual(result[0], {'name': 'a', 'React': '1', 'Angular': '0'})
        self.assertEqual(result[1], {'name': 'b', 'React': '0', 'Angular': '1'})
