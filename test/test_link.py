import unittest

from test.factory import Factory


class TestLink(unittest.TestCase):
    def setUp(self):
        link = Factory.create("Link")
        link.next_link["T"] = Factory.create("Link")
        link.next_link["L"] = Factory.create("Link")
        link.next_link["R"] = Factory.create("Link")
        self.link = link
        self.car = Factory.create("Car")

    def test_add_car_when_car_reach_dead_end(self):
        self.assertFalse(self.link.car_can_proceed(self.car))

    def test_assign_lane_group(self):
        self.car.path = [self.link.link_id, self.link.next_link["T"].link_id]
        self.link.assign_lane_group(self.car)
        self.assertEquals("T", self.car.lane_group)

if __name__ == '__main__':
    unittest.main()