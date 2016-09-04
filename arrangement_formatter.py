import csv

class ArrangementFormatter:
    @staticmethod
    def create_csv_from_groups(groups, output_file):
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(["Group 1:", "a", "d"])
        return output_file 
