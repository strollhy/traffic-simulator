import unittest
from reader import car_reader, link_reader, link2link_reader, signal_reader, path_reader
from test.factory import Factory


class TestLinkData(unittest.TestCase):
    def setUp(self):
        self.link_reader = link_reader.LinkReader()
        self.link2link_reader = link2link_reader.Link2LinkReader()

        self.links = {}
        for link in self.link_reader.links:
            if link.link_id in self.links:
                print "Dup link: %s" % link.link_id
            self.links[link.link_id] = link

    def test_link_data_match(self):
        visited_link = {}
        for link2link in self.link2link_reader.link2links:
            if link2link.link_id in visited_link:
                print "Dup link2link: %s vs %s" % (visited_link[link2link.link_id], link2link)
            else:
                visited_link[link2link.link_id] = link2link

            if link2link.link_id not in self.links:
                self.alert_missing(link2link.link_id)
            if link2link.left_link_id and link2link.left_link_id not in self.links:
                self.alert_missing(link2link.left_link_id)
            if link2link.right_link_id and link2link.right_link_id not in self.links:
                self.alert_missing(link2link.right_link_id)
            if link2link.through_link_id and link2link.through_link_id not in self.links:
                self.alert_missing(link2link.through_link_id)

    def alert_missing(self, link_id):
        print "Missing link: %d" % link_id

    def test_od_data(self):
        file = open("../data/od.csv")
        for l in file:
            link_id = int(l.split(",")[0])
            if link_id not in self.links:
                print link_id

if __name__ == '__main__':
    unittest.main()