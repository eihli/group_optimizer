import csv
from functools import reduce

class ArrangementFormatter:
    @staticmethod
    def create_csv_from_groups(groups, output_file):
        csv_writer = csv.writer(output_file)
        for i, group in enumerate(groups):
            csv_writer.writerow(['Group ' + str(i) + ':', ''] + _get_group_header(group))
        return output_file 

def _get_group_header(group):
    return list(map(lambda p: str(p['id']) + ': ' + p['name'], group))


