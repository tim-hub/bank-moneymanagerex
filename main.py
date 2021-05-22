import sqlite3
import pprint
import csv
import os
from sqlite3 import Cursor
from typing import Tuple

from db.db import get_trans_id, get_transcode, get_account_id_through_details, get_payee_cat_sub_id_through_details
from models.Transcode import Transcode
from utils import get_date_in_string

pp = pprint.PrettyPrinter(indent=2)



def bulk_insert(cur:Cursor, inserting_list):


    INSERT_QUERY = '''
        INSERT INTO CHECKINGACCOUNT_V1
    (TRANSID, ACCOUNTID, TOACCOUNTID, PAYEEID, TRANSCODE, TRANSAMOUNT, TRANSACTIONNUMBER, CATEGID, SUBCATEGID, TRANSDATE, FOLLOWUPID, TOTRANSAMOUNT, NOTES)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);
    '''

    cur.executemany(INSERT_QUERY, list(map(lambda x: tuple(x.values()), inserting_list)))
    # for t in list(map(lambda x: tuple(x.values()), inserting_list)):
    #     cur.execute(INSERT_QUERY, t)







def get_inseting_list(cur: Cursor, file_path: str, account_id, tran_id):
    anz_path = file_path
    pp.pprint(anz_path)

    inserting_list = []

    # opening the file using "with" statement
    with open(anz_path, 'r') as data:

        account_id = account_id
        for row in reversed(list(csv.DictReader(data))):


            tran_id += 1
            to_account_id = -1
            trans_code = get_transcode(cur, str(row['Type']).lower())
            assert Transcode != None
            amount = float(row['Amount'])
            trans_date = get_date_in_string(row['Date'] if 'Date' in row else row['TransactionDate'])
            to_trans_amount = 0 # default 0, if not transfer
            details = str(row['Details']).lower()
            details = 'nan' if details =='' else details
            details = ' '.join(details.split())

            to_account = get_account_id_through_details(cur, details)
            payee_cat_sub = get_payee_cat_sub_id_through_details(cur, details)

            if (trans_code == str(Transcode.Transfer) or ( to_account!=None and payee_cat_sub == None)):
                # Transfer
                # dt = get_date_in_string(d['Date'] if d['Date'] else d['ProcessDate'])
                if (amount < 0):
                    """Only care about transfer out"""
                    to_account_id = to_account[0]
                    trans_amount = abs(amount)
                    to_trans_amount = abs(amount)  # todo multi currency exchange rate here
                    payee_id = -1
                    cat_id = 16 # default hardcode trasnfer category
                    sub_cat_id = -1
                    trans_code = str(Transcode.Transfer)
                else:
                    # ignore transfer in
                    pass

            else:

                trans_amount = abs(amount)
                trans_code = str(Transcode.Deposit) if amount >0 else str(Transcode.Withdraw)
                to_account_id = -1
                try:
                    payee_id, cat_id, sub_cat_id = payee_cat_sub
                except:
                    print(payee_cat_sub)
                    print(details)
                    print(row)

            to_insert = {
                'TRANSID': tran_id,
                'ACCOUNTID': account_id,
                'TOACCOUNTID': to_account_id,
                'PAYEEID': payee_id,
                'TRANSCODE': str(trans_code),
                'TRANSAMOUNT': trans_amount,
                'TRANSACTIONNUMBER': None,
                'CATEGID': cat_id,
                'SUBCATEGID': sub_cat_id,
                'TRANSDATE': trans_date,
                'FOLLOWUPID': -1,
                'TOTRANSAMOUNT': to_trans_amount,
                'NOTES': str(row),
            }

            inserting_list.append(to_insert)
            # pp.pprint(inserting_list)
        return inserting_list

# connect db
con = sqlite3.connect('./data/data.test1.mmb', timeout=10)
cur = con.cursor()
tran_id = get_trans_id(cur)


# get CSV records as input
a2 = get_inseting_list(cur, './data/a.csv', 2, tran_id)
a3 = get_inseting_list(cur, './data/b.csv', 3, tran_id + len(a2))
a4 = get_inseting_list(cur, './c.csv', 4, tran_id + len(a2) + len(a3))
credit = get_inseting_list(cur, './data/d.csv', 19, tran_id + len(a2) + len(a3)+ len(a4))


inserting_all = a2+ a3+a4+credit

# with open('./output_all.csv', 'w') as csv_file:
#     dr = csv.DictWriter(csv_file, inserting_all[0].keys())
#     dr.writeheader()
#     dr.writerows(inserting_all)

bulk_insert(cur, inserting_all)

cur.close()
con.commit()
con.close()

