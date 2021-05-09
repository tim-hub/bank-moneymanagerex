from sqlite3 import Connection, Cursor


def create_detail_to_account(cur: Cursor) -> None:
    query = '''
    CREATE TABLE IF NOT EXISTS details_to_account (
        ID INTEGER PRIMARY KEY,
        DETAILS TEXT NOT NULL,
        ACCOUNT INTEGER NOT NULL
    )
    '''
    cur.execute(query)