import unittest

from utils import get_date_in_string


class MyTestCase(unittest.TestCase):
    def test_date(self):

        self.assertEqual(get_date_in_string('01/01/2020'), '2020-01-01')


if __name__ == '__main__':
    unittest.main()
