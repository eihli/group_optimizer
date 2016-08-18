import time
import logging
from . import csv2json
from . import arrangement2csv
from .arrangement import Arrangement

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
