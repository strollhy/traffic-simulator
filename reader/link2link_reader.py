import csv
from data_reader import DataReader
from model.link2link import Link2Link
from helper.attribute_helper import AttributeHelper

LINK2LINKS = '../data/link2link.csv'


class Link2LinkReader(DataReader):

    def __init__(self, filename=LINK2LINKS):
        super(Link2LinkReader, self).__init__(filename)

        self._link2links = None

    @property
    def link2links(self):
        if self._link2links is None:
            self._link2links = []
            for row in self:
                self._link2links.append(self.create_link2link(row))
        return self._link2links

    @staticmethod
    def create_link2link(args):
        return AttributeHelper.assign_attribute(Link2Link(), args)


if __name__ == "__main__":
    reader = Link2LinkReader(LINK2LINKS)

    import pprint
    pprint.pprint(reader.link2links)
