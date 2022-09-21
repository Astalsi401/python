import re
import logging
from os.path import dirname, abspath
from myfuc import readCsv, List
from requests import get, exceptions
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
from tryRequest import updateProxies, checkProxy, getProxy


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
tmp = f'{pwd}/.tmp'
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


def pageDl(page):
    while True:
        try:
            res = get(f'http://www.tmica.org.tw/directory.php?page={page}', headers=header, proxies=getProxy(tmp), timeout=30)
            with open(f'{pwd}/html/page{page}.html', mode='w+', encoding='utf-8') as f:
                f.write(res.text)
            logging.info('Page:', page, 'Success')
        except exceptions.Timeout:
            continue
        except Exception as e:
            logging.info(page, e)
        break


def getLinks():
    # updateProxies(tmp)
    #checkProxy([{'path': tmp, 'proxy': proxy} for proxy in readCsv(tmp, 'proxies.csv')])
    page = [i for i in range(1, 84)]
    with Pool(6) as pool:
        pool.map(pageDl, page)


def getInfo(page):
    soup = bs(open(f'{pwd}/html/page{page}.html', encoding='utf-8'), 'html.parser')
    keep = ['統一編號', '公司地址', 'TEL', '營業種類']
    info = [{
        'name': e.select('.text h2')[0].text.split(' ')[0],
        'info':e.select('.text div')[0].text.replace('  ', '').split('\n')
    } for e in soup.select('.association')]
    res = []
    for i in info:
        row = {
            'name': i['name'],
            '統一編號': '',
            '公司地址': '',
            'TEL': '',
            '營業種類': '',
        }
        for c in i['info']:
            if f'{keep[0]}：' in c:
                row[keep[0]] = c.replace(f'{keep[0]}：', '')
            elif f'{keep[1]}：' in c:
                row[keep[1]] = c.replace(f'{keep[1]}：', '')
            elif f'{keep[2]}：' in c:
                row[keep[2]] = c.replace(f'{keep[2]}：', '')
            elif f'{keep[3]}：' in c:
                row[keep[3]] = c.replace(f'{keep[3]}：', '')
        res.append([row['name'], row['公司地址'], '', '', row['TEL'], '', '臺北市醫療器材商業同業公會', ''])
    return res


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, filename=f'{pwd}/running.log')
    # getLinks()
    page = [i for i in range(1, 84)]
    with Pool(6) as pool:
        results = pool.map(getInfo, page)
    List(colname + [row for rows in results for row in rows]).writeCsv(pwd, 'orgInfo.csv')
