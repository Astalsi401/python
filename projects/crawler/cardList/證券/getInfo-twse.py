import re
from os.path import dirname, abspath
from bs4 import BeautifulSoup as bs
from myfuc import List, readCsv
from tryRequest import pageDl, updateProxies, checkProxy
from multiprocessing import Pool
from requests import get

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
tmp = f'{pwd}/tmp'
html = f'{pwd}/html'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
colname = ['公司名稱', '住址', '姓名', '職稱', '總機電話', '電子郵件信箱', '市場', '產業類別', '其他來源分類']


def getLinks():
    res = get('https://www.twse.com.tw/zh/brokerService/brokerServiceAudit', headers=header)
    soup = bs(res.text, 'html.parser')
    List([[
        tr.select('td:nth-child(2) a')[0].text,
        'https://www.twse.com.tw' + tr.select('td:nth-child(2) a')[0]['href'],
        tr.select('td:nth-child(4)')[0].text,
        tr.select('td:nth-child(5)')[0].text.replace(' ', ''),
    ] for tr in soup.select('#table2 tbody tr')]).writeCsv(pwd, 'orgLinks.csv')


def main():
    # updateProxies(tmp)
    #checkProxy([{'proxy': proxy, 'path': tmp} for proxy in readCsv(tmp, 'proxies.csv')])
    with Pool(6) as pool:
        pool.map(pageDl, [{'url': link[1], 'filePath': f'{html}/{link[0]}.html', 'proxyPath': tmp} for link in readCsv(pwd, 'orgLinks.csv')])


def getInfo(link):
    soup = bs(open(f'{html}/{link[0]}.html', encoding='utf-8'), 'html.parser')
    tr = soup.select('#table5 table tr')
    return [
        [tr[1].select('td')[0].text.replace(' ', ''), link[2], tr[11].select('td')[0].text.replace(' ', ''), '負責人', link[3], '', '證券'],
        [tr[1].select('td')[0].text.replace(' ', ''), link[2], tr[12].select('td')[0].text.replace(' ', ''), '總經理', link[3], '', '證券'],
    ]


def main1():
    with Pool(6) as pool:
        results = pool.map(getInfo, readCsv(pwd, 'orgLinks.csv'))
    List([colname] + [row for data in results for row in data]).writeCsv(pwd, 'orgInfo.csv')


if __name__ == '__main__':
    main1()
