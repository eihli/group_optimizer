import unittest
from grouping_algo.arrangement import Arrangement
from ..group import Group
from ..participant import Participant
import os
import json

class ArrangementTestCase(unittest.TestCase):
    pass
    def setUp(self):
        f = open('grouping_algo/sample_data/affinities.json')
        survey = json.load(f)
        self.default_json_arrangement = {
            "technical_refusals": {
                "a": ["d"],
                "b": [],
                "c": ["f"],
                "d": ["a"],
                "e": [],
                "f": []
            },
            "interpersonal_refusals": {
                "a": [],
                "b": [],
                "c": [],
                "d": [],
                "e": [],
                "f": ["c"]
                },
            "affinities": {
                "a": ["f"],
                "b": [],
                "c": [],
                "d": ["c"],
                "e": [],
                "f": []
            }
        }

    def test_optimize(self):
        arrangement = Arrangement(self.default_json_arrangement)
        arrangement.optimize()
        self.assertEqual(arrangement.calculate_score(), 2)

    def test_get_unhappiest_group(self):
        a = Arrangement(self.default_json_arrangement, 2)
        self.assertEqual(a.get_unhappiest_group(), a.groups[2])

    def test_makes_best_swap_from_unhappiest_group(self):
        a = Arrangement(self.default_json_arrangement, 2)
        self.assertEqual(a.calculate_score(), -400)
        a.makeBestSwapFromUnhappiestGroup()
        self.assertEqual(a.calculate_score(), -200)
        a.makeBestSwapFromUnhappiestGroup()
        self.assertEqual(a.calculate_score(), 1)

