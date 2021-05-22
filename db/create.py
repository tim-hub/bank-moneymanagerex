from sqlite3 import Cursor

"""
Table between detail to ToAccountID
"""


def create_table_detail_to_account(cur: Cursor) -> None:
    # cur.execute('    DROP TABLE IF EXISTS details_to_account;')
    query = '''
    CREATE TABLE IF NOT EXISTS details_to_account (
        ID INTEGER PRIMARY KEY,
        DETAILS TEXT NOT NULL,
        ACCOUNTID INTEGER NOT NULL,
        UNIQUE (DETAILS, ACCOUNTID)
    );
    '''
    cur.execute(query)

def create_table_detail_to_account_name(cur: Cursor) -> None:
    # cur.execute('    DROP TABLE IF EXISTS details_to_account;')
    query = '''
    CREATE TABLE IF NOT EXISTS details_to_account_name (
        ID INTEGER PRIMARY KEY,
        DETAILS TEXT NOT NULL,
        ACCOUNTNAME TEXT NOT NULL,
        UNIQUE (DETAILS, ACCOUNTNAME)
    );
    '''
    cur.execute(query)

def create_table_detail_to_payee_and_categ_and_subcateg(con: Cursor) -> None:
    query = '''
    CREATE TABLE IF NOT EXISTS details_to_payee (
        DETAILS TEXT NOT NULL PRIMARY KEY,
        PAYEENAME TEXT NOT NULL,
        CATEGNAME TEXT NOT NULL,
        SUBCATEGNAME TEXT NULL
    )
    '''
    con.execute(query)