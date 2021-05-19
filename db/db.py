from sqlite3 import Cursor
from typing import Tuple

INSERT_QUERY = '''
    INSERT INTO CHECKINGACCOUNT_V1
(TRANSID, ACCOUNTID, TOACCOUNTID, PAYEEID, TRANSCODE, TRANSAMOUNT, TRANSACTIONNUMBER, NOTES, CATEGID, SUBCATEGID, TRANSDATE, FOLLOWUPID, TOTRANSAMOUNT)
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);
'''

# def create_table_detail_to_payee(con: Cursor) -> None:
#     query = '''
#     CREATE TABLE IF NOT EXISTS details_to_payee (
#         ID INTEGER PRIMARY KEY,
#         DETAILS TEXT NOT NULL,
#         PAYEE INTEGER NOT NULL
#     )
#     '''
#     con.execute(query)


def insert_payee(cur: Cursor, name: str, cat_id: int, sub_id: int) -> int:
    r = cur.execute('''
    INSERT INTO PAYEE_V1
    (PAYEENAME, CATEGID, SUBCATEGID)
    VALUES (?,?,?)
    ''', (name, cat_id, sub_id))

    return r.rowcount


def insert_details_to_account(cur: Cursor, details: str, to_account_id: int) -> int:
    r = cur.execute('''
    INSERT INTO details_to_account
    (DETAILS, ACCOUNTID)
    VALUES (?,?)
    ''', (details, to_account_id))
    return r.rowcount

def insert_details_to_account_from_details_and_account_name(cur: Cursor, details: str, account_name: str) -> int:
    r = cur.execute('''
INSERT INTO details_to_account(DETAILS, ACCOUNTID)

SELECT ?, ACCOUNTID
FROM ACCOUNTLIST_V1
WHERE ACCOUNTNAME = ?
LIMIT 1
    ''', (details, account_name))
    return r.rowcount


def get_trans_id(cur: Cursor) -> int:
    r = cur.execute('''
SELECT TRANSID
FROM CHECKINGACCOUNT_V1 ORDER BY TRANSID DESC LIMIT 1;
    ''').fetchone()

    return r[0]


def get_transcode(cur:Cursor, t: str) -> str:
    r = cur.execute('''
    SELECT TRANSCODE FROM type_to_transcode
    WHERE TRANSTYPE = '%s'
    ''' % t).fetchone()
    return r[0] if r else None

"""
Return None if cannot find
"""


def get_payee(cur: Cursor, payee_name: str) -> (str, int, int) or None:
    r = cur.execute('''
    SELECT PAYEENAME, CATEGID, SUBCATEGID FROM PAYEE_V1
    WHERE PAYEENAME = '%s'
    ''' % payee_name).fetchall()
    return None if len(r) != 1 else r[0]


def get_account_id(cur: Cursor, name: str) -> int or None:
    r = cur.execute('''
    SELECT ACCOUNTID FROM ACCOUNTLIST_V1
    WHERE ACCOUNTNAME = '%s'
    ''' % name).fetchall()
    return None if len(r) != 1 else r[0][0]


"""
Get Cat and SubCat Id, pass sub cat name as empty if not required
"""


def get_cat_and_sub_cat_id_by_name(cur: Cursor, cat_name: str, sub_cat_name: str = '') -> (int, int):
    cat = cur.execute('''
    SELECT CATEGID FROM CATEGORY_V1
    WHERE CATEGNAME = '%s'
    ''' % cat_name).fetchall()

    if (len(cat) != 1):
        """Cannot find category"""
        return (-2, -1)

    if (sub_cat_name == ''):
        """Subcategory not required"""
        return (cat[0][0], -1)

    sub_cat = cur.execute('''
    SELECT SUBCATEGID, CATEGID FROM SUBCATEGORY_V1
    WHERE SUBCATEGNAME = '%s'
    ''' % sub_cat_name).fetchall()

    if (len(sub_cat) > 0 and sub_cat[0][1] != cat[0][0]):
        """Category and sub category does not match"""
        return (-2, -2)

    if (len(sub_cat) != 1):
        """Cannot find sub category, even category exist"""
        return (cat[0][0], -2)

    return (cat[0][0], sub_cat[0][0])
