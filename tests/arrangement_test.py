import unittest
from group_optimizer.arrangement import Arrangement
import os
import json
import math

class ArrangementTestCase(unittest.TestCase):
    def setUp(self):
        self.default_json_arrangement = [
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

    def test_optimize(self):
        arrangement = Arrangement(self.default_json_arrangement, 2)
        arrangement.optimize()
        self.assertEqual(arrangement.get_score(), 2)

    def test_get_unhappiest_group(self):
        a = Arrangement(self.default_json_arrangement, 2)
        self.assertEqual(a.get_unhappiest_group(), a.groups[2])

    def test_makes_best_swap_from_unhappiest_group(self):
        a = Arrangement(self.default_json_arrangement, 2)
        self.assertEqual(a.get_score(), -400)
        a.make_best_swap_from_unhappiest_group()
        self.assertEqual(a.get_score(), -200)
        a.make_best_swap_from_unhappiest_group()
        self.assertEqual(a.get_score(), 1)

    def test_randomize(self):
        """This is a test to catch regressions and may intermittently fail.
        We are calling #randomize a large number of times and keeping track
        of the location of participant 'a'. I have chosen some arbitrary values
        for the number of samples and an acceptable variation that gives
        me confidence #randomize is working.

        TODO: Look into the math behind calculating a confidence interval
        that a sample is random. If we flip coin 100 times and get 65 heads,
        how confident can we be that the coin is 'fair' (50/50)?
        """
        participants_per_group = 2
        arrangement = Arrangement(
            self.default_json_arrangement,
            participants_per_group
        )
        num_participants = len(arrangement.participants)
        position_counts = {}
        # Initialize position counts
        for i in range(num_participants):
            position_counts[i] = 0
        num_samples = 100
        for i in range(num_samples):
            arrangement.randomize()
            groups = arrangement.groups
            # Flatten groups for easy participant selection by single index
            participants = reduce(lambda g1, g2: g1+g2, groups)
            for idx, p in enumerate(participants):
                if p['name'] == 'a':
                    position_counts[idx] += 1
        mean = float(sum(position_counts.values()) / max(num_participants, 1))
        squared_differences = map(lambda x: (x - mean)**2, position_counts.values())
        variance = sum(squared_differences) / max(num_participants, 1)
        std_dev = math.sqrt(variance)
        expected_max_std_dev = 6
        self.assertTrue(std_dev < expected_max_std_dev,
            "Expected std_dev of {} participants divided ".format(num_participants) +
            "into {} groups over {} samples to be < {} but got {}".format(
                len(arrangement.groups),
                num_samples,
                expected_max_std_dev,
                std_dev))

