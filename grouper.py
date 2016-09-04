import sys
from pathlib import Path
root = str(Path(__file__).resolve().parents[1])
sys.path.append(root)

from grouping_algo.arrangement import Arrangement
from grouping_algo.arrangement_formatter import ArrangementFormatter

class Grouper:
    def __init__(self):
        self.csv = None

    @staticmethod
    def group(input_filename, output_filename, num_participants_per_group = 4):
        with open(input_filename, 'r') as survey_responses:
            arrangement_dict = ArrangementFormatter.create_arrangement_from_csv(survey_responses)
            arrangement = Arrangement(arrangement_dict, num_participants_per_group)
            arrangement.optimize()

        with open(output_filename, 'w') as csv_file:
            ArrangementFormatter.create_csv_from_groups(arrangement.groups, csv_file)

