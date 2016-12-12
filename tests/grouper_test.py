import unittest
import time
import os
import csv
import shutil
import random
from functools import reduce
from tempfile import TemporaryFile
from group_optimizer.grouper import Grouper
from group_optimizer.arrangement_formatter import ArrangementFormatter
from group_optimizer.arrangement import Arrangement

class GrouperTestCase(unittest.TestCase):
    def setUp(self):
        self.csv_file = TemporaryFile('w+')
        csv_writer = csv.writer(self.csv_file)
        csv_writer.writerow(['', 'a', 'b', 'c', 'd', 'e', 'f'])
        csv_writer.writerow(['a', '', '', '', '-1', '', '1'])
        csv_writer.writerow(['b', '', '', '', '', '-1', ''])
        csv_writer.writerow(['c', '', '', '', '1', '', ''])
        csv_writer.writerow(['d', '-1', '', '', '', '', ''])
        csv_writer.writerow(['e', '', '', '', '', '', ''])
        csv_writer.writerow(['f', '1', '', '', '', '', ''])
        self.csv_file.seek(0)

    def tearDown(self):
        self.csv_file.close()

    def test_optimize(self):
        arrangement_list = ArrangementFormatter.create_arrangement_from_csv(
            self.csv_file)
        arrangement = Arrangement(arrangement_list, 2)
        grouper = Grouper(2, arrangement)
        score = grouper.optimize()
        self.assertEqual(score, -97)
        score = grouper.optimize()
        self.assertEqual(score, 2)

    def test_randomize(self):
        # This is currently delegating to Arrangement#randomize
        # and this test is different but redundant.
        # The idea with this test is to randomly select a participant
        # and then see how many randomizations we have to do to see that
        # same participant in the same location. Values chosen are
        # are currently arbitrary.
        arrangement_list = ArrangementFormatter.create_arrangement_from_csv(
            self.csv_file)
        arrangement = Arrangement(arrangement_list, 2)
        grouper = Grouper(2, arrangement)
        # Flatten groups
        participants = reduce(lambda g1, g2: g1+g2, grouper.arrangement.groups)
        idx_to_track = random.randint(0, len(participants)-1)
        participant_to_track = participants[idx_to_track]
        appearance_count = 1
        goal_appearance_count = 10
        attempt_count = 0
        min_num_attempts_considered_success = 25
        max_num_attempts_considered_success = 75
        break_guard = 1000
        while appearance_count < goal_appearance_count:
            if attempt_count > break_guard:
                break
            participants = reduce(lambda g1, g2: g1+g2, grouper.arrangement.groups)
            if participants[idx_to_track] == participant_to_track:
                appearance_count += 1
            grouper.randomize()
            attempt_count += 1
        assertion_message = "Expected between {} and {} randomizations " + \
            "to see participant with name {} appear at position {} " + \
            "but it appeared {} times in {} attempts."
        assertion_message = assertion_message.format(
            min_num_attempts_considered_success,
            max_num_attempts_considered_success,
            participant_to_track['name'],
            idx_to_track,
            appearance_count,
            attempt_count)
        self.assertTrue(attempt_count < max_num_attempts_considered_success,
            assertion_message)

class GrouperStaticTestCase(unittest.TestCase):
    """Tests the static #group method

    This method reads, optimizes, and writes to file.
    It is being deprecated in favor of allowing more granular control
    over how a group is optimized.
    """

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

class GrouperFileTestCase(unittest.TestCase):
    def setUp(self):
        self.out_file = TemporaryFile('w+')
        self.csv_file = TemporaryFile('w+')
        csv_writer = csv.writer(self.csv_file)
        csv_writer.writerow(['', 'a', 'b', 'c', 'd', 'e', 'f'])
        csv_writer.writerow(['a', '', '', '', '-1', '', '1'])
        csv_writer.writerow(['b', '', '', '', '', '-1', ''])
        csv_writer.writerow(['c', '', '', '', '1', '', ''])
        csv_writer.writerow(['d', '-1', '', '', '', '', ''])
        csv_writer.writerow(['e', '', '', '', '', '', ''])
        csv_writer.writerow(['f', '1', '', '', '', '', ''])
        self.csv_file.seek(0)

    def tearDown(self):
        self.out_file.close()
        self.csv_file.close()

    def test_optimize(self):
        arrangement_list = ArrangementFormatter.create_arrangement_from_csv(
            self.csv_file)
        arrangement = Arrangement(arrangement_list, 2)
        grouper = Grouper(2, arrangement)
        score = grouper.optimize()
        self.assertEqual(score, -97)
        score = grouper.optimize()
        self.assertEqual(score, 2)
