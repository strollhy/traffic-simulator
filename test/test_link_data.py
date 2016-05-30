import unittest
from reader import car_reader, link_reader, link2link_reader, signal_reader, path_reader
from test.factory import Factory


class TestLinkData(unittest.TestCase):
    def setUp(self):
        self.link_reader = link_reader.LinkReader()
        self.link2link_reader = link2link_reader.Link2LinkReader()

        self.links = {}
        for link in self.link_reader.links:
            self.links[link.link_id] = link

    def test_link_data_match(self):
        for link2link in self.link2link_reader.link2links:
            link_id = link2link.link_id
            self.assertIn(link_id, self.links)


if __name__ == '__main__':
    unittest.main()