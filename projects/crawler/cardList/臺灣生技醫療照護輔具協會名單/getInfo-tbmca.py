from asyncio import proactor_events
import re
import logging
from os.path import dirname, abspath
from urllib import request
from requests import get, exceptions
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
from tryRequest import updateProxies, checkProxy, pageDl
from myfuc import List, readCsv

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
tmp = f'{pwd}/tmp'
html = f'{pwd}/html'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
colname = [[
    '公司名稱',
    '住址',
    '姓名',
    '職稱',
    '總機電話',
    '電子郵件信箱',
    '市場',
    '產業類別',
    '其他來源分類'
]]


def getLinkPage():
    for p in range(1, 3):
        res = get(f'http://tbmca.com.tw/member?page={p}')
        with open(f'{html}/page{p}.html', encoding='utf-8', mode='w+') as f:
            f.write(res.text)


def main():
    for p in range(1, 3):
        soup = bs(open(f'{html}/page{p}.html', encoding='utf-8'), 'html.parser')
        List([[
            tr.select('td')[1].text,
            tr.select('td')[2].text,
            tr.select('td')[3].text,
            'http://tbmca.com.tw' + tr.select('td:nth-child(5) a')[0]['href'],
        ] for tr in soup.select('.table.table-hover tbody tr')]).writeCsv(pwd, 'orgLinks.csv', mode='a+')


def main2():
    # updateProxies(tmp)
    #checkProxy([{'proxy': proxy, 'path': tmp} for proxy in readCsv(tmp, 'proxies.csv')])
    with Pool(6) as pool:
        pool.map(pageDl, [{
            'url': link[-1],
            'filePath': f'{pwd}/html/{link[0]}.html',
            'proxyPath': tmp
        } for link in readCsv(pwd, 'orgLinks.csv')])


def getInfo(link):
    soup = bs(open(f'{html}/{link[0]}.html', encoding='utf-8'), 'html.parser')
    tr = soup.select('#Dyn_2_2 table.table.table-hover tr')
    return [
        link[0].replace(' ', ''),
        link[2],
        tr[2].select('td')[3].text.replace(' ', ''),
        '負責人',
        link[1],
        tr[4].select('td')[1].text,
        '臺灣生技醫療照護輔具協會名單',
        '',
        '',
    ]


def main3():
    with Pool(6) as pool:
        results = pool.map(getInfo, readCsv(pwd, 'orgLinks.csv'))
    List(colname + results).writeCsv(pwd, 'orgInfo.csv')


if __name__ == '__main__':
    main3()
