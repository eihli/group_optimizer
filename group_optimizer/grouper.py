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
class Grouper:
    """A representation of the grouping arrangement
    and functions for optimizing groups.

    -current_score - Numeric representation of the 'goodness' of an arrangement.
    A function of the 'goodness' of each group.

    #optimize - runs optimization on arrangement, mutating arrangement and
    updating current_score
    """

    def __init__(self, in_file, num_participants_per_group = DEFAULT_PARTICIPANTS_PER_GROUP):
        self.csv = None
        self.arrangement_dict = ArrangementFormatter.create_arrangement_from_csv(in_file)
        self.arrangement = Arrangement(self.arrangement_dict, num_participants_per_group)
        self.last_score = float('-inf')
        self.current_score = self.arrangement.get_score()

    # TODO: Deprecate. This calls arrangement's #optimize which will do full optimization
    @staticmethod
    def group(input_filename, output_filename, num_participants_per_group = 4):
        with open(input_filename, 'r') as survey_responses:
            arrangement_dict = ArrangementFormatter.create_arrangement_from_csv(survey_responses)
            arrangement = Arrangement(arrangement_dict, num_participants_per_group)
            arrangement.optimize()

        with open(output_filename, 'w') as csv_file:
            ArrangementFormatter.create_csv_from_groups(arrangement.groups, csv_file)

    # Perform a single optimization swap
    def optimize(self):
        self.arrangement.make_best_swap_from_unhappiest_group()
        self.last_score = self.current_score
        self.current_score = self.arrangement.get_score()
        return self.current_score

    def randomize(self):
        random.shuffle(self.arrangement_dict)
        self.arrangement = Arrangement(self.arrangement_dict, DEFAULT_PARTICIPANTS_PER_GROUP)

    def is_optimized(self):
        return self.last_score == self.arrangement.get_score()

