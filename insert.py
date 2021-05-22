from sqlite3 import Cursor


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


def insert_details_to_payee(cur:Cursor, details:str ,payee_name: str, categ_name: str, subcateg_name: str):
    r = cur.execute('''
    INSERT INTO details_to_payee(DETAILS, PAYEENAME, CATEGNAME, SUBCATEGNAME)

    SELECT ?, ?, 
    cat.CATEGNAME,
    CASE
        WHEN s.SUBCATEGNAME IS NULL THEN NULL 
        ELSE s.SUBCATEGNAME
    END AS SUBCATEGNAME
    
    FROM CATEGORY_V1 as cat
    LEFT JOIN  SUBCATEGORY_V1 as s
    ON s.CATEGID = cat.CATEGID
    WHERE (cat.CATEGNAME = ? AND (s.SUBCATEGNAME = ? OR s.SUBCATEGNAME IS NULL))
    ORDER BY cat.CATEGNAME ASC 
    LIMIT 1
    
    ''', (details, payee_name, categ_name, subcateg_name))
    return r.rowcount


"""
Which details name are different with payee name
"""
def insert_to_payeelist(cur: Cursor, payee_name: str, categ_name: str, subcateg_name: str) -> int:
    r = cur.execute('''
INSERT INTO PAYEE_V1(PAYEENAME, CATEGID, SUBCATEGID)

SELECT ?,
    cat.CATEGID,  
    CASE
        WHEN s.SUBCATEGID IS NULL THEN -1
        ELSE s.SUBCATEGID
    END AS SUBCATEGID

FROM CATEGORY_V1 as cat
LEFT JOIN  SUBCATEGORY_V1 as s
ON s.CATEGID = cat.CATEGID
WHERE cat.NAME = ? AND (s.SUBCATEGNAME = ? OR s.SUBCATEGNAME IS NULL)
ORDER BY cat.CATEGNAME ASC 
LIMIT 1
    ''', (payee_name, categ_name, subcateg_name))
    return r.rowcount