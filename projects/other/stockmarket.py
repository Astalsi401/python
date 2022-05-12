import requests
import csv
import time

stock = []
market = '興櫃'
dl = 'EMG'
with open(f'D:/Documents/work/櫃買市場募資/{market}.csv', newline='') as f:
    rows = csv.reader(f)
    for row in rows:
        stock.append(row)
for a in stock:
    response = requests.get(
        f'https://www.tpex.org.tw/web/regular_emerging/statistics/fund_raising/dl.php?l=zh-tw&t={dl}&DOC_ID={a[0]}')
    with open(f'D:/Documents/Data/pyinstall/{a[1]}.xls', 'wb') as file:
        file.write(response.content)
        file.close()
        print(f'{a[1]} saved')
        time.sleep(1)

# https://www.tpex.org.tw/web/regular_emerging/statistics/fund_raising/dl.php?l=zh-tw&t=EMG&DOC_ID=301
