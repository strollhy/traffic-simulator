from data_reader import DataReader

LINKS = '../data/link.csv'


class LinkReader(DataReader):

    def __init__(self, path):
        super(LinkReader, self).__init__(path)

        self._links = None

    @property
    def links(self):
        if self._links is None:
            self._links = []
            for row in self:
                self._links.append(row)
        return self._links


if __name__ == "__main__":
    reader = LinkReader(LINKS)

    import pprint
    pprint.pprint(reader.links)
