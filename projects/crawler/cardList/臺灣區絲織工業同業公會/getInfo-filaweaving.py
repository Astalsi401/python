from time import sleep
from requests import get
from myfuc import writeJson, List
from os.path import dirname, abspath
from json import load
import re

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
json = f'{pwd}/json'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}


def getData(page):
    res = get(f'https://www.filaweaving.org.tw/index.php?s=xls_import&a=fetch&page={page}&limit=15&pages=10', cookies={'PHPSESSID': 'qd9ojuuqpetgk602ci0dtlp8g5'}, headers=header).json()
    writeJson(json, f'page{page}.json', res['data'])
    sleep(10)


def main1():
    for page in range(1, 11):
        getData(page)


def main2():
    res = [['公司名稱', '地址', '姓名', '職稱', '總機電話', '電子郵件', '市場', '產業類別', '其他來源分類']]
    for page in range(1, 11):
        for row in load(open(f'{json}/page{page}.json', encoding='utf-8-sig')):
            content = row['content']
            res.append([content['公司名稱_中'], content['公司地址_中'], content['負責人'], '負責人', content['公司電話'], content['EMAIL'], '臺灣區絲織工業同業公會', '', ''])
            res.append([content['公司名稱_中'], content['公司地址_中'], content['總經理'], '總經理', content['公司電話'], content['EMAIL'], '臺灣區絲織工業同業公會', '', ''])
    List(res).writeCsv(pwd, 'orgInfo.csv')


if __name__ == '__main__':
    main2()
