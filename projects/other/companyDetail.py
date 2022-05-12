import codecs
import requests
import sys
import time


pwd = 'D:/Documents/Data/pyinstall/companyDataBase'
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
}
data = []
cap = ['F', 'G']

for w in cap:
    print(f'cap {w}')
    for i in range(0, 500000, 1000):
        url = f'https://data.gcis.nat.gov.tw/od/data/api/F0E8FB8D-E2FD-472E-886C-91C673641F31?$format=json&$filter=Company_Status%20eq%2001%20and%20Capital_Stock_Amount%20eq%20{w}&$skip={i}&$top=1000'
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        time.sleep(0.2)
        if res.text != '':
            data.append(res.text.replace('[', '').replace(']', ''))
            print(f'append {i}')
        else:
            break
with open(f'{pwd}/company.json', 'w', encoding='UTF-8') as f:
    f.write('[')
    index = 1
    for i in data:
        if index != len(data):
            f.write(f'{i},')
            print(f'write data[{index}]')
        else:
            f.write(i)
            print(f'write data[{index}]')
        index = index + 1
    f.write(']')
