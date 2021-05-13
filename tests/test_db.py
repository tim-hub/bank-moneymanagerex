import unittest
import sqlite3
from db import create_table_detail_to_account, get_trans_id, get_cat_and_sub_cat_id_by_name, insert_payee, \
    insert_details_to_account, get_account_id, get_transcode


class DBTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.con = sqlite3.connect('../data/data.test.mmb')
        self.cursor = self.con.cursor()

    def tearDown(self) -> None:
        self.con.commit()
        self.cursor.close()

    def test_always_true(self):
        self.assertEqual(True, True)

    # def test_creat_table_details_to_payee(self):
    #     create_table_detail_to_payee(self.cursor)
    #
    #     self.cursor.execute('''
    #     SELECT name FROM sqlite_master WHERE type='table' AND name='details_to_payee';
    #     ''')
    #
    #     r = self.cursor.fetchall()
    #
    #     self.assertEqual(len(r), 1)

    def test_creat_table_details_to_account(self):
        create_table_detail_to_account(self.cursor)

        self.cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='details_to_account';
        ''')

        r = self.cursor.fetchall()

        self.assertEqual(len(r), 1)

    def test_get_transID(self):
        r = get_trans_id(self.cursor)
        self.assertGreaterEqual(r, 2168)

    def test_get_cat_and_sub_cat_ids_with_proper_category_and_subcategory_names(self):
        r = get_cat_and_sub_cat_id_by_name(self.cursor, 'Food', 'Groceries')
        self.assertEqual(r, (2, 8))

    def test_get_cat_and_sub_cat_ids_with_proper_category_name_and_no_sub_category(self):
        r = get_cat_and_sub_cat_id_by_name(self.cursor, 'Food', '')
        self.assertEqual(r, (2, -1))

    def test_get_cat_and_sub_cat_ids_with_proper_category_name_and_wrong_sub_category(self):
        r = get_cat_and_sub_cat_id_by_name(self.cursor, 'Food', 'Groc')
        self.assertEqual(r, (2, -2))

    def test_get_cat_and_sub_cat_ids_with_wrong_category_name_and_proper_sub_category(self):
        r = get_cat_and_sub_cat_id_by_name(self.cursor, 'Food1', 'Groceries')
        self.assertEqual(r, (-2, -1))

    def test_get_cat_and_sub_cat_ids_with_wrong_category_name_and_proper_sub_category(self):
        r = get_cat_and_sub_cat_id_by_name(self.cursor, 'Food', 'Water')
        self.assertEqual(r, (-2, -2))

    def test_insert_one_payee(self):
        r = insert_payee(self.cursor, 'test_payee', 2, 8)
        self.assertEqual(r, 1)
        self.cursor.execute(
            '''
            DELETE FROM PAYEE_V1 WHERE PAYEENAME = '%s'
            ''' % 'test_payee'
        )

    def test_insert_one_details_to_account(self):
        r = insert_details_to_account(self.cursor, 'test_details', 1)
        self.assertEqual(r, 1)
        self.cursor.execute(
            '''
            DELETE FROM details_to_account WHERE DETAILS = '%s'
            ''' % 'test_details'
        )

    def test_get_account(self):
        r = get_account_id(self.cursor, 'NZ cash')
        self.assertEqual(r,1)

    def test_get_transcode_by_code(self):
        r = get_transcode(self.cursor, 'Salary')
        self.assertEqual(r, 'Deposit')


    def test_get_transcode_by_code_with_wrong_type_name(self):
        r = get_transcode(self.cursor, 'Salary1')
        self.assertEqual(r, None)

if __name__ == '__main__':
    unittest.main()
