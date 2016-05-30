import unittest
from reader import car_reader, link_reader, link2link_reader, signal_reader, path_reader
from model.sublink1 import SubLink1
from model.sublink2 import SubLink2
from model.sublink3 import SubLink3


class ReaderTest(unittest.TestCase):
    def setUp(self):
        self.car_reader = car_reader.CarReader()
        self.link_reader = link_reader.LinkReader()
        self.link2link_reader = link2link_reader.Link2LinkReader()
        self.signal_reader = signal_reader.SignalReader()
        self.path_reader = path_reader.PathReader()

    def test_read_car(self):
        self.assertIsNotNone(self.car_reader.cars)

    def test_read_link(self):
        self.assertIsNotNone(self.link_reader.links)

    def test_read_link2link(self):
        self.assertIsNotNone(self.link2link_reader.link2links)

    def test_read_signal(self):
        self.assertIsNotNone(self.signal_reader.signals)

    def test_read_path(self):
        self.assertIsNotNone(self.path_reader.paths)

    def test_car_creation(self):
        for car in self.car_reader.cars:
            self.assertIsInstance(car.car_id, int)
            self.assertIsInstance(car.start_time, int)
            self.assertIsInstance(car.path, list)

    def test_link_creation(self):
        for link in self.link_reader.links:
            self.assertIsInstance(link.link_id, int)
            self.assertIsInstance(link.length, int)
            self.assertIsInstance(link.lanes_num, int)
            self.assertIsInstance(link.min_speed, int)
            self.assertIsInstance(link.max_speed, int)
            self.assertIsInstance(link.max_cap, int)
            self.assertIsInstance(link.jam_density, int)
            self.assertGreater(link.jam_density, 0)
            self.assertIsInstance(link.sublink1, SubLink1)
            self.assertIsInstance(link.sublink2, SubLink2)
            self.assertIsInstance(link.sublink3, SubLink3)

    def test_link2link_creation(self):
        # TODO test link2link
        pass

if __name__ == '__main__':
    unittest.main()