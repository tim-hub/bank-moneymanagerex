import unittest
import sqlite3
from mmb import create_detail_to_account


class DBTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.cursor = sqlite3.connect('../data/data.test.mmb').cursor()

    def test_always_true(self):
        self.assertEqual(True, True)

    def test_creat_table_details_to_account(self):
        create_detail_to_account(self.cursor)

        self.cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='details_to_account';
        ''')

        r = self.cursor.fetchall()

        self.assertEqual(len(r), 1)


if __name__ == '__main__':
    unittest.main()
