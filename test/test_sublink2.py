import unittest
from test.factory import Factory


class TestLink(unittest.TestCase):
    def setUp(self):
        self.link = Factory.create("Link")
        self.cars = [Factory.create("Car") for _ in xrange(3)]

if __name__ == '__main__':
    unittest.main()