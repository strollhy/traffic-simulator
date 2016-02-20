import unittest

from test.factory import Factory


class TestLink(unittest.TestCase):
    def setUp(self):
        self.link = Factory.create("Link")
        self.cars = [Factory.create("Car") for _ in xrange(3)]

    def test_add_car_going_straight(self):
        for car in self.cars:
            car.lane_group = "T"
            self.link.sublink1.add_car(car)
            self.assertNotIn(car, self.link.sublink1.lanes[-1])

    def test_add_car_going_left(self):
        for car in self.cars:
            car.lane_group = "L"
            self.link.sublink1.add_car(car)
            self.assertIn(car, self.link.sublink1.lanes[0])

    def test_add_car_going_right(self):
        for car in self.cars:
            car.lane_group = "R"
            self.link.sublink1.add_car(car)
            self.assertIn(car, self.link.sublink1.lanes[-1])

    def test_release_car_released(self):
        self.link.sublink2.add_car = lambda c, l: True
        for car in self.cars:
            car.lane_group = "T"
            self.link.sublink1.add_car(car)
            self.link.sublink1.release_cars()
            for lane in self.link.sublink1.lanes:
                self.assertNotIn(car, lane)

if __name__ == '__main__':
    unittest.main()