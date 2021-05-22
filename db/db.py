from sqlite3 import Cursor

# INSERT_QUERY = '''
#     INSERT INTO CHECKINGACCOUNT_V1
# (TRANSID, ACCOUNTID, TOACCOUNTID, PAYEEID, TRANSCODE, TRANSAMOUNT, TRANSACTIONNUMBER, NOTES, CATEGID, SUBCATEGID, TRANSDATE, FOLLOWUPID, TOTRANSAMOUNT)
# VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);
# '''
from typing import Tuple


def get_trans_id(cur: Cursor) -> int:
    r = cur.execute('''
SELECT TRANSID
FROM CHECKINGACCOUNT_V1 ORDER BY TRANSID DESC LIMIT 1;
    ''').fetchone()

    return r[0]


def get_transcode(cur:Cursor, t: str) -> str:
    r = cur.execute('''
    SELECT TRANSCODE FROM type_to_transcode
    WHERE TRANSTYPE = ?
    ''', (t,)).fetchone()
    return r[0] if r else None

# def get_account_id_through_details(cur:Cursor, details: str) -> int:
#     r = cur.execute('''
#     SELECT ACCOUNTID FROM details_to_account
#     WHERE DETAILS = ?
#     ''', (details,)).fetchone()
#     return int(r[0]) if r else None


def get_payee_cat_sub_id_through_details(cur:Cursor, details: str) -> Tuple:
    r = cur.execute('''
    SELECT p.PAYEEID, CATEGID, SUBCATEGID 
    FROM details_to_payee as d, PAYEE_V1 as p
    WHERE 
     d.DETAILS = ? AND
     p.PAYEENAME = d.PAYEENAME COLLATE NOCASE 
    LIMIT 1
    ''' , (details,)).fetchone()
    return r if r else None

def get_account_id_through_details(cur:Cursor, details: str) -> Tuple:
    r = cur.execute('''
    SELECT ACCOUNTID
    FROM details_to_account 
    WHERE DETAILS = ? COLLATE NOCASE 
    ''' , (details,)).fetchone()
    return r if r else None


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
