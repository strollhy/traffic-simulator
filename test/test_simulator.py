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
        self.assertEquals(sorted(self.simulator.cars, key=lambda c: c.start_time),
                          self.simulator.cars)
    # TODO add signal tests
    # def test_setup_lights(self):
    #     self.simulator.setup_lights()

if __name__ == '__main__':
    unittest.main()