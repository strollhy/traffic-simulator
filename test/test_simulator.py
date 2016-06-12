import unittest

from main import simulator


class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.simulator = simulator.Simulator()

    def test_setup_links(self):
        self.simulator.setup_links()
        self.assertIsNotNone(self.simulator.links)

    def test_setup_link2links(self):
        self.simulator.setup_links()
        self.simulator.setup_link2links()
        for link in self.simulator.links.values():
            assert link.next_link

    def test_setup_cars(self):
        self.simulator.setup_cars()
        self.assertIsNotNone(self.simulator.cars)
        self.assertEquals(sorted(self.simulator.cars, key=lambda c: c.start_time, reverse=True),
                          self.simulator.cars)

    def test_setup_lights(self):
        self.simulator.setup_links()
        self.simulator.setup_signal()
        for link in self.simulator.links.values():
            if link.type == "normal":
                for lane in link.sublink3.lanes:
                    if not lane.signal:
                        print "Link %s has no %s signal" % (link.link_id, lane.type)

    def test_setup_paths(self):
        self.simulator.setup_paths()
        self.assertIsNotNone(self.simulator.paths.items())

if __name__ == '__main__':
    unittest.main()