import sqlite3
import requests

from log_helper import setup_logging

URLS = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

def fetch_binance():
    '''
    GET 10 transaction VND
    '''
    payload = {"page": 1, "rows": 10, "payTypes": [], "asset": "USDT", "tradeType": "BUY",
               "fiat": "VND", "publisherType": "merchant", "merchantCheck": True}
    headers = {
        'Content-Type': "application/json", }
    response = requests.request(
        "POST", url=URLS, json=payload, headers=headers)

    return response

# TODO decorator
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


def average(lst):
    '''
    Average price VND top 10 users
    '''
    return sum(lst) / len(lst)

# TODO add decorator
def insertDB(conn, price_avg, price_sum):
    conn.execute(
            "insert into transaction_records(price_avg, price_sum) values (?,?)", (price_avg, price_sum))
    return conn.commit()


if __name__ == '__main__':
    logger = setup_logging()
    conn = setup_mysql(logger=logger)
    import pandas as pd
    import matplotlib.pyplot as plt


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

    # MATPLOT
    df = pd.read_csv("./BTC-USD.csv")


    df = df.dropna()


    plt.plot(df['Date'] , df['Close'])
    plt.show()


