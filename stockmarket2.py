import urllib.request  # urllib2.urlopen
import urllib.error
import zipfile  # zipfile.ZipFile
import csv
import time


stock = []
market = '上市'
with open(f'D:/Documents/work/櫃買市場募資/{market}.csv', newline='') as f:
    rows = csv.reader(f)
    for row in rows:
        stock.append(row)
for a in stock:
    # 檔案下載
    downloadurl = urllib.request.urlopen(
        f'https://www.twse.com.tw{a[0]}')
    zipcontent = downloadurl.read()
    with open(f'D:/Documents/Data/pyinstall/{a[1]}.zip', 'wb') as f:
        f.write(zipcontent)
    print(f'{a[1]}.zip saved')
    time.sleep(5)
