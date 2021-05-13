import datetime
def get_date_in_string(d: str) -> str:
    return datetime.datetime.strptime(d, '%d/%m/%Y').strftime('%Y-%m-%d')