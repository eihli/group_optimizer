import unittest
from grouping_algo.arrangement import Arrangement
from ..group import Group
from ..participant import Participant
import os
import pdb
import json

class arrangementTestCase(unittest.TestCase):
    def setUp(self):
        f = open('grouping_algo/sample_data/affinities.json')
        survey = json.load(f)
        self.arrangement = Arrangement(survey)
        self.p1 = Participant("Eric")
        self.p2 = Participant("Sam")
        self.p3 = Participant("Glenn")
        self.p4 = Participant("Taylor")
        self.g1 = Group()
        self.g2 = Group()

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

    def test_arrangement_can_read_from_file(self):
        self.assertEqual(len(self.arrangement.participants), 20)
        self.assertIsInstance(self.arrangement.participants[1], Participant)
        names = map(lambda p: p.name, self.arrangement.participants)
        self.assertIn('Mary Polster', names)

    def test_arrangement_scoring_function(self):
        self.arrangement.groups = []
        group = Group()
        # TODO: Finish arrangement scoring function/tests

    # These next tests are something that should be abstracted out into a strategy
    # We want to be able to swap the each person from the unhappiest group
    # into each other group until and keep the "best" arrangement from those
    # swaps.
    def test_get_unhappiest_group(self):
        json_arrangement = {
            "technical_refusals": {
                "john": ["glenn"],
                "glenn": [],
                "eric": [],
                "sam": []
            },
            "interpersonal_refusals": {
                "john": [],
                "glenn": [],
                "eric": [],
                "sam": []
                },
            "affinities": {
                "eric": ["sam", "glenn"],
                "john": [],
                "sam": [],
                "glenn": []
            }
        }
        a = Arrangement(json_arrangement, 2)
        self.assertEqual(a.getUnhappiestGroup(), a.groups[1])

    # I think I just found a perfect use case for generators and yield
    # I want to loop over each person in a group, swap that person with each
    # person in each other group, and after each swap, check to see
    # the score of the arrangement.
    # We don't want the arrangement score checking code inside this function.
    # https://www.jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/
    def test_makes_best_swap_from_unhappiest_group(self):
        json_arrangement = {
            "technical_refusals": {
                "a": ["d"],
                "b": ["e"],
                "c": [],
                "d": ["a"],
                "e": [],
                "g": []
            },
            "interpersonal_refusals": {
                "a": [],
                "b": [],
                "c": [],
                "d": [],
                "e": [],
                "g": []
                },
            "affinities": {
                "a": ["c"],
                "b": ["g"],
                "c": ["b"],
                "d": [],
                "e": [],
                "g": ["b"]
            }
        }
        a = Arrangement(json_arrangement, 2)
        a.makeBestSwapFromUnhappiestGroup()
        self.assertEqual(a.calculateScore(), -99)
        a.makeBestSwapFromUnhappiestGroup()
        self.assertEqual(a.calculateScore(), 1)

