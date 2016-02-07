import unittest
from reader import car_reader, link_reader, link2link_reader


class TestReader(unittest.TestCase):
    def setUp(self):
        self.car_reader = car_reader.CarReader()
        self.link_reader = link_reader.LinkReader()
        self.link2link_reader = link2link_reader.Link2LinkReader()

    def test_read_car(self):
        assert self.car_reader.cars

    def test_read_link(self):
        assert self.link_reader.links

    def test_read_link2link(self):
        assert self.link2link_reader.link2links

    def test_car_creation(self):
        for car in self.car_reader.cars:
            assert car.car_id
            assert car.start_time
            assert car.path

if __name__ == '__main__':
    unittest.main()