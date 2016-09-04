import unittest
import time
import os
import csv
import shutil
from ..grouper import Grouper

class GrouperTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = 'tmp' + str(time.time())
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        with open(self.tmp_dir + '/input.csv', 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['', 'a', 'b', 'c', 'd', 'e', 'f'])
            csv_writer.writerow(['a', '', '', '', '-1', '', '1'])
            csv_writer.writerow(['b', '', '', '', '', '-1', ''])
            csv_writer.writerow(['c', '', '', '', '1', '', ''])
            csv_writer.writerow(['d', '-1', '', '', '', '', ''])
            csv_writer.writerow(['e', '', '', '', '', '', ''])
            csv_writer.writerow(['f', '1', '', '', '', '', ''])

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)


    def test_group(self):
        Grouper.group(self.tmp_dir + '/input.csv', self.tmp_dir + '/output.csv', 2)
        self.assertTrue(os.path.exists(self.tmp_dir + '/output.csv'), "Expected 'group' to create output file but none existed")
        with open(self.tmp_dir + '/output.csv', 'r') as result_file:
            csv_reader = csv.reader(result_file)
            first_row = next(csv_reader)
            self.assertEqual(first_row, ['Group 0:', '', '0: a', '5: f'])

            second_row = next(csv_reader)
            self.assertEqual(second_row, ['', '0: a', '', '1'])
