from collections import namedtuple
import datetime
import requests
CURRENCY_PAIRS = ('BTC_ETH', 'BTC_ZEC', 'BTC_LBC')






def main():
    for CURRENCY_PAIR in CURRENCY_PAIRS:
        d = []
        data__currency_pair = get_data_currency_pair(CURRENCY_PAIR)
        for item in data__currency_pair:
            date, time = convert_time(item['date'])
            d.append({
                'tiсker': CURRENCY_PAIR,
                'per': 5,
                'date': date,
                'time': time,
                'open': item['open'],
                'high': item['high'],
                'low': item['low'],
                'close': item['close'],
                'vol': item['volume']
            })
        print(d)
        save_file(CURRENCY_PAIR, d)
        


def get_data_currency_pair(currency_pairs):
    resp = requests.get('https://poloniex.com/public?command=returnChartData&currencyPair={}&start=64543&end=9999999999&period=300'.format(currency_pairs))
    assert resp.ok
    return resp.json()


def convert_time(unix_date):
    date = datetime.datetime.fromtimestamp(
        int(unix_date)
    ).strftime('%Y%m%d %H%M%S')

    d = date.split(' ')[0]
    t = date.split(' ')[1]

    return d, t

def save_file(name, d):
    thefile = open('{}.txt'.format(name), 'w')
    thefile.write('<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>')

    for item in d:
        thefile.write('{},{},{},{},{},{},{},{},{}\n'.format(item['tiсker'],
                                                          item['per'],
                                                          item['date'],
                                                          item['time'],
                                                          item['open'],
                                                          item['high'],
                                                          item['low'],
                                                          item['close'],
                                                          item['vol']))

    thefile.close()

main()
