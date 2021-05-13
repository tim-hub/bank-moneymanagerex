import sqlite3
import pprint
import csv
import os
from sqlite3 import Cursor

from db import get_trans_id, get_transcode
from models.Transcode import Transcode
from utils import get_date_in_string

pp = pprint.PrettyPrinter(indent=2)




def bulk_insert(cur: Cursor, file_path: str):
    anz_path = file_path
    pp.pprint(anz_path)

    inserting_list = []

    INSERT_QUERY = '''
        INSERT INTO CHECKINGACCOUNT_V1
    (TRANSID, ACCOUNTID, TOACCOUNTID, PAYEEID, TRANSCODE, TRANSAMOUNT, TRANSACTIONNUMBER, NOTES, CATEGID, SUBCATEGID, TRANSDATE, FOLLOWUPID, TOTRANSAMOUNT)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);
    '''

    # opening the file using "with" statement
    with open(anz_path, 'r') as data:
        tran_id = get_trans_id(cur)
        for row in reversed(list(csv.DictReader(data))):
            print(row)
            tran_id += 1
            to_insert = {
                'TRANSID': tran_id,
                'ACCOUNTID': 0,
                'TOACCOUNTID': 0,
                'PAYEEID': 0,
                'TRANSCODE': str(Transcode.Withdraw),
                'TRANSAMOUNT': 0,
                'TRANSACTIONNUMBER': None,
                'NOTES': str(row),
                'CATEGID': -1,
                'SUBCATEGID': -1,
                'TRANSDATE': get_date_in_string(row['Date'] if row['Date'] else row['ProcessDate']),
                'FOLLOWUPID': -1,
                'TOTRANSAMOUNT': 0,
            }


            trans_code = get_transcode(row['Type'])

            if (row['Type'] == 'Transfer'):
                """anz transfer"""
                amount = int(row['Amount'])
                # dt = get_date_in_string(d['Date'] if d['Date'] else d['ProcessDate'])
                if (amount < 0):
                    """Only care about transfer out"""
                    to_insert['TRANSAMOUNT'] = abs(amount)
                    to_insert['TOTRANSAMOUNT'] = abs(amount)  # todo multi currency exchange rate here

                to_insert['TRANSCODE'] = Transcode.Transfer

            # elif (row['Type'] == 'Transfer'):


# connect db
con = sqlite3.connect('./data/data.test.mmb')

# get CSV records as input
anz_path =  './data/' + os.listdir('./data')[6]


bulk_insert(con.cursor(), anz_path)