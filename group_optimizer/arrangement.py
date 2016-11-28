import sys
import random
from pathlib import Path
root = str(Path(__file__).resolve().parents[1])
sys.path.append(root)

import json
import math
from functools import reduce

DEFAULT_NUM_INDIVIDUALS = 4
MAX_ITERATIONS = 100

class Arrangement:
    def __init__(self, json_arrangement, num_individuals_per_group = DEFAULT_NUM_INDIVIDUALS):
        self.groups = []
        self.participants = json_arrangement

        # 9.0 / 4 = 2.25 = 3 Groups of 3 people each
        # TODO: Allow other grouping logic. Perhaps we want 1 group of 4 and 1 group of 5
        num_groups = int(math.ceil(float(len(self.participants)) / num_individuals_per_group))

        for i in range(num_groups):
            self.groups.append([])

        for i, participant in enumerate(self.participants):
            self.groups[i % num_groups].append(participant)

    def optimize(self, prev_score = None, count = 0):
        self.make_best_swap_from_unhappiest_group()
        cur_score = self.get_score()
        if cur_score == prev_score or count > MAX_ITERATIONS:
            return self.groups
        count += 1
        self.optimize(cur_score, count)

    def randomize(self):
        """Randomize participants in groups"""
        # Flatten groups. This lets us select by a participant by a single number.
        participants = reduce(lambda g1, g2: g1+g2, self.groups)
        for i in range(len(participants)-1):
            p1 = participants[i]
            rand_idx = random.randint(i+1, len(participants)-1)
            p2 = participants[rand_idx]
            self._swap_individuals(p1, p2)

    def get_score(self):
        total = 0
        for group in self.groups:
            total += self._get_group_score(group)
        return total

    def make_best_swap_from_unhappiest_group(self):
        best_gain = 0
        best_swap = (None, None)
        unhappiest_group = self.get_unhappiest_group()
        for participant1 in unhappiest_group:
            for group in self.groups:
                if group != unhappiest_group:
                    for participant2 in group:
                        oldScore = self.get_score()
                        self._swap_individuals(participant1, participant2)
                        newScore = self.get_score()
                        if newScore > oldScore:
                            best_gain = newScore - oldScore
                            best_swap = (participant1, participant2)
                        self._swap_individuals(participant1, participant2)
        if best_swap[0] != None:
            self._swap_individuals(best_swap[0], best_swap[1])
        return best_gain

    def get_unhappiest_group(self):
        # This reduce makes things more confusing and harder to read.
        group = reduce(lambda g, a: g if self._get_group_score(g) < self._get_group_score(a) else a, self.groups)
        return group

    def _swap_individuals(self, a, b):
        a_group_index = self._find_group_index_for_participant(a)
        b_group_index = self._find_group_index_for_participant(b)
        a_group = self.groups[a_group_index]
        b_group = self.groups[b_group_index]

        a_index = self._find_participant_index_in_group(a_group, a)
        b_index = self._find_participant_index_in_group(b_group, b)
        temp_a = a_group[a_index]
        temp_b = b_group[b_index]

        self.groups[a_group_index][a_index] = temp_b
        self.groups[b_group_index][b_index] = temp_a

    def _find_group_index_for_participant(self, p):
        for idx, group in enumerate(self.groups):
            if p in group:
                return idx

    def _find_participant_index_in_group(self, g, p):
        for idx, participant in enumerate(g):
            if participant == p:
                return idx

    def __repr__(self):
        result = ''
        average_group_score = reduce(lambda x, y: x + self._get_group_score(y), self.groups, 0) / len(self.groups)
        result += "Arrangement with Score: " + str(self.get_score()) + " "
        result += "with average score: " + str(average_group_score) + '\n'
        result += '\nGroups:\n'
        i = 0
        for group in self.groups:
            result += "Group " + str(i) + "\n"
            result += group + '\n'
            i += 1
        result += '\n'
        return result

    def _get_group_score(self, group):
        score = 0
        for participant1 in group:
            for participant2 in group:
                if participant1['id'] != participant2['id']:
                    if participant2['id'] in participant1['affinities']:
                        score += 1
                    if participant2['id'] in participant1['technical_refusals']:
                        score -= 100
                    if participant2['id'] in participant1['interpersonal_refusals']:
                        score -= 100
        return score


