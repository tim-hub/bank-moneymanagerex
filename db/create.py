from sqlite3 import Cursor

"""
Table between detail to ToAccountID
"""


def create_table_detail_to_account(cur: Cursor) -> None:
    cur.execute('    DROP TABLE IF EXISTS details_to_account;')
    query = '''
    CREATE TABLE IF NOT EXISTS details_to_account (
        ID INTEGER PRIMARY KEY,
        DETAILS TEXT NOT NULL,
        ACCOUNTID INTEGER NOT NULL,
        UNIQUE (DETAILS, ACCOUNTID)
    );
    '''
    cur.execute(query)