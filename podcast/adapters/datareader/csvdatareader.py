import csv


class CSVDataReader:
    def __init__(self, podcasts_file, episodes_file):
        self.podcasts_file = podcasts_file
        self.episodes_file = episodes_file

    def get_podcasts(self):
        with open(self.podcasts_file, 'r') as file:
            reader = csv.DictReader(file)
            podcasts_data = [row for row in reader]
        return podcasts_data

    def get_episodes(self):
        with open(self.episodes_file, 'r') as file:
            reader = csv.DictReader(file)
            episodes_data = [row for row in reader]
        return episodes_data
