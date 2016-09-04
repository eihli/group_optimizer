import json
import math
from functools import reduce
from .participant import Participant

class Arrangement:
    def __init__(self, json_arrangement, num_individuals_per_group = 4):
        self.groups = []
        self.participants = json_arrangement

        numGroups = math.ceil(1.0 * len(self.participants) / num_individuals_per_group)

        for i in range(numGroups):
            self.groups.append([])

        i = 0
        for participant in self.participants:
            self.groups[i % numGroups].append(participant)
            i += 1

    def optimize(self):
        self.make_best_swap_from_unhappiest_group()
        self.make_best_swap_from_unhappiest_group()

    def calculate_score(self):
        total = 0
        for group in self.groups:
            total += self._get_group_score(group)
        return total

    def make_best_swap_from_unhappiest_group(self):
        bestGain = 0
        bestSwap = (None, None)
        unhappiest_group = self.get_unhappiest_group()
        global_old_score = self.calculate_score()
        for participant1 in unhappiest_group:
            for group in self.groups:
                if group != unhappiest_group:
                    for participant2 in group:
                        oldScore = self.calculate_score()
                        self._swap_individuals(participant1, participant2)
                        newScore = self.calculate_score()
                        if newScore >= oldScore:
                            bestGain = newScore - oldScore
                            bestSwap = (participant1, participant2)
                        self._swap_individuals(participant1, participant2)
        if bestSwap[0] != None:
            self._swap_individuals(bestSwap[0], bestSwap[1])
            global_new_score = self.calculate_score()
        return bestGain

    def _create_participants(self, json_arrangement):
        for idx, participant in json_arrangement.items():
            self.participants[idx] = name
        for key, name in self.participants.items():
            for json_arrangementType in json_arrangement:
                self.participants[key][json_arrangementType] = []
                for target_name in json_arrangement[json_arrangementType][name]:
                    # set their affinity
                    self.participants[key][json_arrangementType].append()
                    participant.affinityDict[json_arrangementType](self.get_participant(name))

    def get_participant(self, name):
        return next(p for p in self.participants if p.name == name)

    def read_participants_from_file(self, filename):
        f = open(filename)
        survey = json.load(f)
        for name in survey['technical_refusals']:
            self.participants.append(Participant(name))
        for participant in self.participants:
            for surveyType in survey:
                for name in survey[surveyType][participant.name]:
                    # set their affinity
                    # print((participant.name + ' ' + surveyType + ' ' + name))
                    participant.affinityDict[surveyType](self.get_participant(name))

    def load_participants_from_json(self, jsonString):
        survey = json.loads(jsonString)
        # Doesn't matter which survey we use here.
        # We just need a list of all names
        for name in survey['technical_refusals']:
            self.participants.append(Participant(name))
        for participant in self.participants:
            set_affinities(survey, participant)

    @staticmethod
    def set_affinities(survey, participant):
        for surveyType in survey:
            for name in survey[surveyType][participant.name]:
                participant.affinityDict[surveyType](self.get_participant(name))

    def get_unhappiest_group(self):
        group = reduce(lambda g, a: g if self._get_group_score(g) < self._get_group_score(a) else a, self.groups)
        return group

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

    def _swap_individuals(self, a, b):
        aGroupIndex = self._find_group_index_for_participant(a)
        bGroupIndex = self._find_group_index_for_participant(b)
        aGroup = self.groups[aGroupIndex]
        bGroup = self.groups[bGroupIndex]

        aIndex = self._find_participant_index_in_group(aGroup, a)
        bIndex = self._find_participant_index_in_group(bGroup, b)
        temp_a = aGroup[aIndex]
        temp_b = bGroup[bIndex]

        self.groups[aGroupIndex][aIndex] = temp_b
        self.groups[bGroupIndex][bIndex] = temp_a

    def _find_group_index_for_participant(self, p):
        for idx, group in enumerate(self.groups):
            if p in group:
                return idx

    def _find_participant_index_in_group(self, g, p):
        for idx, participant in enumerate(g):
            if participant == p:
                return idx


    def makeBestSwap(self):
        for i in range(len(self.groups)):
            for p1 in self.groups[i].participants:
                for j in range(len(self.groups)):
                    if not i == j:
                        for p2 in self.groups[j].participants:
                            self._swap_individuals(p1, p2)

    def __repr__(self):
        result = ''
        averageGroupScore = reduce(lambda x, y: x + self._get_group_score(y), self.groups, 0) / len(self.groups)
        i = 0
        result += "Arrangement with Score: " + str(self.score) + " "
        result += "with average score: " + str(averageGroupScore) + '\n'
        result += 'Participants:\n'
        for participant in self.participants:
            result += participant.name + ', '
        result = result[:-2] + '\nGroups:\n'
        for group in self.groups:
            result += "Group " + str(i) + "\n"
            result += group.__repr__() + '\n'
            i += 1
        result += '\n'
        return result

