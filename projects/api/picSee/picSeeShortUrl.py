from requests import post
from myfuc import readCsv, writeCsv
from os.path import dirname, abspath
from time import sleep
from json import load
import pandas as pd
import re

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))


def shortUrl(url):
    json = {
        "url": url,
        "externalId": "inno",
        "applySubdomain": False
    }
    limit = 10
    key = load(open(f'{pwd}/secret/key.json'))['key']
    while True:
        try:
            res = post(f'https://api.pics.ee/v1/links/?access_token={key}', json=json).json()
        except:
            if limit < 10:
                limit += 1
                continue
            else:
                print('error:', url)
                break
        break
    sleep(0.1)
    try:
        return res['data']['picseeUrl']
    except KeyError:
        print(res)
        return res['error']['message']


def main():
    data = []
    for i in ['企業', '初創', '國際', '學研1', '學研2', '臨床'][:1]:
        data += readCsv(f'{pwd}/secret/csv', f'get links - {i}.csv')[1:]
    #writeCsv(f'{pwd}/secret/output', 'picSeeShort.csv', [['雲端路徑', '檔案/資料夾名稱', '原始連結', 'picSee短網址']], mode='w+')
    for r in data:
        res = shortUrl(r[4])
        r.append(res)
        writeCsv(f'{pwd}/secret/output', 'picSeeShort.csv', [[r[0], r[1], r[4], r[9]]], mode='a+')


def xlsx():
    df = pd.read_csv(f'{pwd}/secret/output/picSeeShort.csv')
    df.to_excel(f'{pwd}/secret/output/picSeeShort.xlsx', index=False)
