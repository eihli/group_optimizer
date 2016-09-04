import csv
from functools import reduce

class ArrangementFormatter:
    @staticmethod
    def create_arrangement_from_csv(csv_file):
        csv_reader = csv.reader(csv_file)
        header_row = next(csv_reader)[1:]
        arrangement = []
        for idx, participant in enumerate(header_row):
            arrangement.append({
                'id': idx,
                'name': participant,
                'technical_refusals': [],
                'interpersonal_refusals': [],
                'affinities': []
            })

        for participant1_id, row in enumerate(csv_reader):
            participant1 = reduce(lambda x, y: y if y['id'] == participant1_id and x == None else x, arrangement, None)
            row = row[1:]
            for participant2_id, survey_response in enumerate(row):
                if survey_response:
                    if int(survey_response) < 0:
                        participant1['technical_refusals'].append(participant2_id)
                    else:
                        participant1['affinities'].append(participant2_id)
        return arrangement

    @staticmethod
    def create_csv_from_groups(arrangement, groups, output_file):
        csv_writer = csv.writer(output_file)
        for i, group in enumerate(groups):
            csv_writer.writerow(['Group ' + str(i) + ':', ''] + _get_group_header(group))
            for participant in group:
                csv_writer.writerow(_get_participant_row(participant, group, arrangement))
        return output_file 

def _get_group_header(group):
    return list(map(lambda p: str(p['id']) + ': ' + p['name'], group))

def _get_participant_row(participant, group, arrangement):
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
