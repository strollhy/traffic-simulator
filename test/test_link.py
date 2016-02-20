import unittest

from model.car import Car
from test.factory import Factory


class TestLink(unittest.TestCase, ):
    def setUp(self):
        link = Factory.create("Link")
        link.next_link["T"] = Factory.create("Link")
        link.next_link["L"] = Factory.create("Link")
        link.next_link["R"] = Factory.create("Link")
        self.link = link

        car = Car()
        car.path = []
        self.car = car

    def test_add_car_when_car_reach_deadend(self):
        self.assertFalse(self.link.car_can_proceed(self.car))

    def test_assign_lane_group(self):
        self.car.path = [self.link.link_id, self.link.next_link["T"].link_id]
        self.link.assign_lane_group(self.car)
        self.assertEquals("T", self.car.lane_group)

if __name__ == '__main__':
    unittest.main()