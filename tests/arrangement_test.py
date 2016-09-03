import unittest
from grouping_algo.arrangement import Arrangement
from ..group import Group
from ..participant import Participant
import os
import json

class arrangementTestCase(unittest.TestCase):
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
        self.arrangement = Arrangement(survey)
        self.p1 = Participant("Eric")
        self.p2 = Participant("Sam")
        self.p3 = Participant("Glenn")
        self.p4 = Participant("Taylor")
        self.g1 = Group()
        self.g2 = Group()

    def test_optimize(self):
        arrangement = Arrangement(self.default_json_arrangement)
        arrangement.optimize()
        self.assertEqual(arrangement.calculateScore(), 2)


    def test_arrangement_get_participant(self):
        self.arrangement.addParticipant(self.p1)
        participant = self.arrangement.getParticipant('Eric')
        self.assertIsInstance(self.arrangement.getParticipant('Eric'), Participant)

    def test_arrangement_add_participant(self):
        self.arrangement.addParticipant(self.p1)
        self.assertIsInstance(self.arrangement.participants[0], Participant)

    def test_arrangement_can_add_participant_to_group(self):
        self.arrangement.groups[0] = self.g1
        self.arrangement.addParticipantToGroup(self.p1, self.g1)
        self.assertIs(self.arrangement.groups[0].participants[0], self.p1)
        self.assertIs(self.p1.group, self.g1)

    def test_arrangement_scoring_function(self):
        self.arrangement.groups = []
        group = Group()
        # TODO: Finish arrangement scoring function/tests

    def test_get_unhappiest_group(self):
        a = Arrangement(self.default_json_arrangement, 2)
        self.assertEqual(a.getUnhappiestGroup(), a.groups[2])

    def test_makes_best_swap_from_unhappiest_group(self):
        a = Arrangement(self.default_json_arrangement, 2)
        self.assertEqual(a.calculateScore(), -400)
        a.makeBestSwapFromUnhappiestGroup()
        self.assertEqual(a.calculateScore(), -200)
        a.makeBestSwapFromUnhappiestGroup()
        self.assertEqual(a.calculateScore(), 1)

