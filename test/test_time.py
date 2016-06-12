import unittest

from model.time import Time


class TestTime(unittest.TestCase):
    def setUp(self):
        self.time = Time()

    def test_singleton(self):
        self.assertEquals(self.time, Time())

    def test_update_time(self):
        current_time = Time().time
        Time().update_time()
        self.assertEquals(current_time + 10, Time().time)


if __name__ == '__main__':
    unittest.main()