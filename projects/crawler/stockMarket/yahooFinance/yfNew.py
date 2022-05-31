import random
import time
import datetime
import pandas as pd
import urllib.request

pwd = 'D:\Documents\work\產業研究\生醫上市櫃\pythonCsv'
period1 = int(time.mktime(datetime.datetime(1979, 12, 31, 23, 59).timetuple()))
period2 = int(time.mktime(datetime.datetime(2022, 12, 31, 23, 59).timetuple()))
interval = '1d'  # 1d, 1m
stockId = open('stockIdEdit.txt', 'r')
print(stockId)


for sid in stockId:
    try:
        link = f'https://query1.finance.yahoo.com/v7/finance/download/{sid}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
        urllib.request.urlopen(link).code
    except Exception as err:
        print(err)
    else:
        df = pd.read_csv(link)
        df.to_csv(f'{pwd}\{sid}.csv')
        print(f'{sid}.csv saved')
        time.sleep(1)
