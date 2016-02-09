import unittest
from reader import car_reader, link_reader, link2link_reader
from model.sublink1 import SubLink1
from model.sublink2 import SubLink2
from model.sublink3 import SubLink3


class TestReader(unittest.TestCase):
    def setUp(self):
        self.car_reader = car_reader.CarReader()
        self.link_reader = link_reader.LinkReader()
        self.link2link_reader = link2link_reader.Link2LinkReader()

    def test_read_car(self):
        self.assertIsNotNone(self.car_reader.cars)

    def test_read_link(self):
        self.assertIsNotNone(self.link_reader.links)

    def test_read_link2link(self):
        self.assertIsNotNone(self.link2link_reader.link2links)

    def test_car_creation(self):
        for car in self.car_reader.cars:
            self.assertIsInstance(car.car_id, int)
            self.assertIsInstance(car.start_time, int)
            self.assertIsInstance(car.path, list)

    def test_link_creation(self):
        for link in self.link_reader.links:
            self.assertIsInstance(link.link_id, int)
            self.assertIsInstance(link.length, int)
            self.assertIsInstance(link.num_of_lanes, int)
            self.assertIsInstance(link.min_speed, int)
            self.assertIsInstance(link.max_speed, int)
            self.assertIsInstance(link.max_cap, int)
            self.assertIsInstance(link.jam_density, int)
            self.assertIsInstance(link.sublink1, SubLink1)
            self.assertIsInstance(link.sublink2, SubLink2)
            self.assertIsInstance(link.sublink3, SubLink3)

if __name__ == '__main__':
    unittest.main()