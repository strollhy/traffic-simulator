import csv


class DataReader(object):

    def __init__(self, path):
        self.path = path

    def __iter__(self):
        with open(self.path, 'rU') as data:
            for row in csv.DictReader(data):
                yield row