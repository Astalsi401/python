import logging
import re
from os.path import dirname, abspath
from myfuc import List, readCsv
from bs4 import BeautifulSoup as bs
from requests import get
from tryRequest import updateProxies, checkProxy, getProxy, pageDl
from multiprocessing import Pool

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
htmlPath = f'{pwd}/html'
tmp = f'{pwd}/.tmp'
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


def main1():
    # updateProxies(tmp)
    # checkProxy([{'proxy': proxy, 'path': tmp} for proxy in readCsv(tmp, 'proxies.csv')])
    with Pool(6) as pool:
        pool.map(pageDl, [{
            'url': f'http://www.tfpma.org.tw/zh-TW/member/index.html?page={i}',
            'filePath': f'{htmlPath}/list/page{i}.html',
            'proxyPath': tmp
        } for i in range(1, 15)])


def getLinks():
    List([[corp.text, 'http://www.tfpma.org.tw' + corp['href']] for page in range(1, 15) for corp in bs(open(f'{htmlPath}/list/page{page}.html', encoding='utf-8'), 'html.parser').select('#faqs div.togglet h5 a')]).writeCsv(pwd, 'orgLinks.csv')


def main2():
    updateProxies(tmp)
    checkProxy([{'proxy': proxy, 'path': tmp} for proxy in readCsv(tmp, 'proxies.csv')])
    with Pool(6) as pool:
        pool.map(pageDl, [{
            'url': link[1],
            'filePath': f'{htmlPath}/detail/{link[0]}.html',
            'proxyPath': tmp
        } for link in readCsv(pwd, 'orgLinks.csv')[256:]])


def getInfo(link):
    soup = bs(open(f'{htmlPath}/detail/{link[0]}.html'), 'html.parser')
    res = {
        'corp': link[0],
        'add': [],
        'name': '',
        'pos': '負責人',
        'tel': '',
        'email': '',
        'cat': '臺灣食品暨製藥機械工業同業公會',
        'prod': soup.select('.span9 p')[1].text.replace('\n', '、') if len(soup.select('.span9 p')) >= 2 else '',
    }
    for c in soup.select('.span9 .desc_html ul li'):
        if '地址' in c.text:
            res['add'].append(re.search(r'：\S+', c.text).group().replace('：', ''))
        elif '負責人' in c.text:
            res['name'] = re.search(r'：\S+', c.text).group().replace('：', '')
        elif '電話' in c.text:
            res['tel'] = re.search(r'：\S+', c.text).group().replace('：', '')
        elif '電子信箱' in c.text:
            res['email'] = re.findall(r'\S+@\S+', c.text.replace('電子信箱：', ''))
    return [res['corp'], '、'.join(res['add']), res['name'], res['pos'], res['tel'], '、'.join(res['email']).replace(',', ''), res['cat'], '', res['prod']]


def main3():
    with Pool(6) as pool:
        results = pool.map(getInfo, readCsv(pwd, 'orgLinks.csv'))
    List(colname + results).writeCsv(pwd, 'orgInfo.csv')


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, filename=f'{pwd}/running.log')
    main3()
