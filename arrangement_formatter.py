import csv
from functools import reduce

class ArrangementFormatter:
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
