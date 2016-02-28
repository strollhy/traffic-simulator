import csv


class DataReader(object):

    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        with open(self.filename, 'rU') as data:
            for row in csv.DictReader(data):
                yield row