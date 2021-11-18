import requests
import numpy as np
import yfinance as yf
import h5py
import pandas as pd


link = "https://query1.finance.yahoo.com/v7/finance/download/000004.SZ?period1=662774400&period2=1636070400&interval=1d&events=history&includeAdjustedClose=true"
r = requests.get(link)
data = pd.DataFrame(r.json())
data.to_csv('D:/Documents/Data' + '/stock_id.csv', index=False, header=True)

# 必須先安裝yfinance套件

# 讀取csv檔
stock_list = pd.read_csv('D:/Documents/Data' + '/stock_id.csv')
stock_list.columns = ['STOCK_ID', 'NAME']

historical_data = pd.DataFrame()

for i in stock_list.index:

    # 抓取股票資料
    stock_id = stock_list.loc[i, 'STOCK_ID'] + '.TW'
    data = yf.Ticker(stock_id)
    df = data.history(period="max")

    # 增加股票代號
    df['STOCK_ID'] = stock_list.loc[i, 'STOCK_ID']

    # 合併
    historical_data = pd.concat([historical_data, df])
    time.sleep(0.8)

historical_data.to_hdf('D:/Documents/Data' + '/historical_data.h5', key='s')
