import sys
import random
from pathlib import Path

from group_optimizer.arrangement import Arrangement
from group_optimizer.arrangement_formatter import ArrangementFormatter

DEFAULT_PARTICIPANTS_PER_GROUP = 4

# TODO:
# An arrangement should not know how to score nor optimize itself.
# It should be just a data representation of an arrangement.
# It could be scored many different ways.
class Strategy:
    @staticmethod
    def optimize(arrangement):
        arrangement.make_best_swap_from_unhappiest_group()

class Grouper:
    """A representation of the grouping arrangement
    and functions for optimizing groups.

    -current_score - Numeric representation of the 'goodness' of an arrangement.
    A function of the 'goodness' of each group.

    #optimize - runs optimization on arrangement, mutating arrangement and
    updating current_score
    """

    def __init__(self,
            num_participants_per_group = 4,
            arrangement = None,
            strategy = None):
        self.csv = None
        self.arrangement = arrangement
        self.strategy = strategy or Strategy
        self.last_score = float('-inf')
        self.current_score = self.arrangement.get_score()

    # Perform a single optimization swap
    def optimize(self):
        self.strategy.optimize(self.arrangement)
        self.last_score = self.current_score
        self.current_score = self.arrangement.get_score()
        return self.current_score

    def randomize(self):
        self.arrangement.randomize()

    def is_optimized(self):
        return self.last_score == self.arrangement.get_score()

class CategoryGrouper:
    """Group by category preference"""

    @staticmethod
    def group(individuals, num_groups):
        groups = [[] for x in range(num_groups)]
        for i, individual in enumerate(individuals):
            groups[i % num_groups] = groups[i % num_groups] or []
            groups[i % num_groups].append(i)
        return groups

    def score_group(individuals, group, categories):
        import math
        responses = []
        for category in categories:
            responses.append([individuals[i][category] for i in group])
        print(responses)
