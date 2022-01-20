import logging
import sqlite3
import requests
import sys
from datetime import datetime

#


def fetch_binance():
    '''
    GET 10 transaction VND
    '''
    URLS = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {"page": 1, "rows": 10, "payTypes": [], "asset": "USDT", "tradeType": "BUY",
               "fiat": "VND", "publisherType": "merchant", "merchantCheck": True}
    headers = {
        'Content-Type': "application/json", }
    response = requests.request(
        "POST", url=URLS, json=payload, headers=headers)

    return response


# LOGGING
def setup_logging():
    # Handlers - Formats - Levels
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.FileHandler("appdata")
    log_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.DEBUG)

    # Define LOGGER
    logger = logging.getLogger('APP')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


def setup_mysql(logger):
    """
        Connect to database sqlite
    """
    try:
        con = sqlite3.connect('example.db')
        logger.info('CONNECTION SUCCESS')

        cur = con.cursor()
        cur.execute('''create table if not exists transaction_records
                    (id integer primary key autoincrement,
                    price_avg real,
                    price_sum real,
                    time datetime default current_timestamp)
                    ''')

        logger.info(con.commit)
        return con
    except sqlite3.Error as er:
        logger.error(er)
        pass

    pass


def average(lst):
    '''
    Average price VND top 10 users
    '''
    return sum(lst) / len(lst)


def insertDB(conn, price_avg, price_sum):
    conn.execute(
            "insert into transaction_records(price_avg, price_sum) values (?,?)", (price_avg, price_sum))
    return conn.commit()



if __name__ == '__main__':
    logger = setup_logging()
    conn = setup_mysql(logger=logger)


    response = fetch_binance()
    if response.status_code == 200:
        logger.info(response)
        data = response.json()['data']
        # get price single record
        arr = [float(v['adv']['price']) for v in data]

        # calculation
        price_avg = average(arr)
        price_sum = sum(arr)

        # insert avg price and sum
        insertDB(conn, price_avg, price_sum)
    else:
        logger.error(response)
        pass

    pass

