import os
import pandas as pd
import requests
import sys
sys.path.append('D:/Documents/python/myFunction')
from myfuc import writeCsv, getMopsInfo
from time import sleep


def getMopsInfo(market, ind):
    url = 'https://mops.twse.com.tw/mops/web/t51sb01'
    payload = {
        'encodeURIComponent': '1',
        'step': '1',
        'firstin': '1',
        'TYPEK': f'{market[0]}',
        'code': f'{ind[0]}',
    }
    res = requests.post(url, data=payload)
    sleep(0.5)
    df = []
    for a in pd.read_html(res.text)[9].copy().values.tolist():
        df.append([a[0], a[2], a[3], a[15], a[16], a[17], a[18], a[19]])
    return df


pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/').replace('/py', '')
indust = [['22', '生技醫療'], ['33', '農業科技']]
market = [['sii', '上市'], ['otc', '上櫃'], ['rotc', '興櫃']]
print(getMopsInfo(['sii', '上市'], ['22', '生技醫療']))
for m in market:
    for i in indust:
        data = getMopsInfo(m, i)
