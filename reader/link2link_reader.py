import csv
from data_reader import DataReader

LINK2LINKS = '../data/link2link.csv'


class Link2LinkReader(DataReader):

    def __init__(self, path=LINK2LINKS):
        super(Link2LinkReader, self).__init__(path)

        self._link2links = None

    @property
    def link2links(self):
        if self._link2links is None:
            self._link2links = []
            for row in self:
                self._link2links.append(row)
        return self._link2links


if __name__ == "__main__":
    reader = Link2LinkReader(LINK2LINKS)

    import pprint
    pprint.pprint(reader.link2links)
