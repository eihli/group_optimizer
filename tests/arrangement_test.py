import unittest
from grouping_algo.arrangement import Arrangement
from ..group import Group
from ..participant import Participant
import os
import json

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
        self.assertEqual(arrangement.calculate_score(), 1)

    def test_get_unhappiest_group(self):
        a = Arrangement(self.default_json_arrangement, 2)
        self.assertEqual(a.get_unhappiest_group(), a.groups[2])

    def test_makes_best_swap_from_unhappiest_group(self):
        a = Arrangement(self.default_json_arrangement, 2)
        self.assertEqual(a.calculate_score(), -400)
        a.make_best_swap_from_unhappiest_group()
        self.assertEqual(a.calculate_score(), -200)
        a.make_best_swap_from_unhappiest_group()
        self.assertEqual(a.calculate_score(), 1)

