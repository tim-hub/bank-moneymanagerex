from sqlite3 import Cursor


def create_detail_to_account(cur: Cursor) -> None:
    query = '''
    CREATE TABLE IF NOT EXISTS details_to_account (
        ID INTEGER PRIMARY KEY,
        DETAILS TEXT NOT NULL,
        ACCOUNT INTEGER NOT NULL
    )
    '''
    cur.execute(query)


def create_detail_to_payee(cur: Cursor) -> None:
    query = '''
    CREATE TABLE IF NOT EXISTS details_to_payee (
        ID INTEGER PRIMARY KEY,
        DETAILS TEXT NOT NULL,
        PAYEE INTEGER NOT NULL
    )
    '''
    cur.execute(query)