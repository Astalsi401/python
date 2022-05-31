import pandas as pd
from bs4 import BeautifulSoup
import requests
import codecs
import sys

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

url = 'https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID=4144'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
}
res = requests.get(url, headers=headers)
res.encoding = 'utf-8'
res.text

soup = BeautifulSoup(res.text, 'lxml')
data = soup.find_all("td", attrs={"bgcolor": "white", "colspan": "5"})
for a in data:
    print(a)
