import csv
from functools import reduce

class ArrangementFormatter:
    @staticmethod
    def create_arrangement_from_csv(csv_file):
        # Why is someone giving you an open file that's not seeked?
        csv_file.seek(0)
        csv_reader = csv.reader(csv_file)
        header_row = next(csv_reader)[1:]
        arrangement = []

        # Create an array of Participants as dicts
        # A dict of Participants might be easier to work with in the rest of the code
        # but I think this was done because at some point we needed to maintain/guarantee order
        # as we iterated over arrangement. It can maybe be refactored now.
        for idx, participant in enumerate(header_row):
            arrangement.append({
                'id': idx,
                'name': participant,
                'technical_refusals': [],
                'interpersonal_refusals': [],
                'affinities': []
            })

        for participant1_id, row in enumerate(csv_reader):
            # This reduce can be confusing. This basically just searches the arrangement list to find and return a participant dict.
            participant1 = reduce(lambda x, y: y if y['id'] == participant1_id and x == None else x, arrangement, None)

            # The first element of the row will be the participants name. We only want their responses here.
            row = row[1:]
            for participant2_id, survey_response in enumerate(row):
                if survey_response:
                    if int(survey_response) < 0:
                        participant1['technical_refusals'].append(participant2_id)
                    else:
                        participant1['affinities'].append(participant2_id)
        return arrangement

    @staticmethod
    def create_csv_from_groups(groups, output_file):
        csv_writer = csv.writer(output_file)
        for i, group in enumerate(groups):
            csv_writer.writerow(['Group ' + str(i) + ':', 'Happiness Score: ' + str(_get_group_score(group))] + _get_group_header(group))
            for participant in group:
                csv_writer.writerow(_get_participant_row(participant, group))
        return output_file

# TODO: Clean this up
def _get_group_score(group):
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

def _get_group_header(group):
    return list(map(lambda p: str(p['id']) + ': ' + p['name'], group))

def _get_participant_row(participant, group):
    header_columns = _get_group_header(group)
    row = []
    for column in header_columns:
        value = ''
        target_id = int(column.split(':')[0])
        if target_id in participant['technical_refusals']:
            value = '-1'
        if target_id in participant['interpersonal_refusals']:
            value = '-1'
        if target_id in participant['affinities']:
            value = '1'
        row.append(value)
    row = ['', str(participant['id']) + ': ' + participant['name']] + row
    return row
