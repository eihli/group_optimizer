import sys
from pathlib import Path
root = str(Path(__file__).resolve().parents[1])
sys.path.append(root)

import time
import logging
from arrangement import Arrangement
from arrangement_formatter import ArrangementFormatter

NUM_ITERATIONS = 10
TIMEOUT = 200

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname) %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class Grouper:
    def __init__(self):
        self.csv = None

    @staticmethod
    def group(input_filename, output_filename):
        with open(input_filename, 'r') as survey_responses:
            arrangement_dict = ArrangementFormatter.create_arrangement_from_csv(survey_responses)
            arrangement = Arrangement(arrangement_dict)
            arrangement.optimize()

        with open(output_filename, 'w') as csv_file:
            ArrangementFormatter.create_csv_from_groups(arrangement.groups, csv_file)

def swap_unhappiest(arrangement):
    previous_score_improvement = float('inf')
    arrangement.randomizeGroups()
    start_time = end_time = time.time()
    while (end_time - start_time < TIMEOUT and
            previous_score_improvement != 0):
        previous_score_improvement = arrangement.makeBestSwap()
        logger.debug(arrangement)
        print(previous_score_improvement)
        arrangement.score = arrangement.calculateScore()
    return arrangement

def perform(csv_file):
    json_arrangement = csv2json(csv_file)

    arrangements = [Arrangement(jsonString = json_arrangement)
                    for x in range(NUM_ITERATIONS)]

    results = []
    for arrangement in arrangements:
        results.append(swap_unhappiest(arrangement))
        results = sorted(results, key = lambda x: x.score)
        logger.debug(results[-3:])

    arrangement2csv(results[-1], csv_file + '_result.csv')
