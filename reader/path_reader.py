from data_reader import DataReader
from model.path import Path
from helper.attribute_helper import AttributeHelper

PATHS = '../data/output/allocation_path.csv'


class PathReader(DataReader):
    def __init__(self, filename=PATHS):
        super(PathReader, self).__init__(filename)

        self._paths = None

    @property
    def paths(self):
        if self._paths is None:
            self._paths = []
            for row in self:
                self._paths.append(self.create_path(row))
        return self._paths

    @staticmethod
    def create_path(args):
        args['nodes'] = [int(n) for n in args['nodes'].split('-')]
        return AttributeHelper.assign_attribute(Path(), args)

if __name__ == "__main__":
    reader = PathReader()

    import pprint
    pprint.pprint(reader.paths)