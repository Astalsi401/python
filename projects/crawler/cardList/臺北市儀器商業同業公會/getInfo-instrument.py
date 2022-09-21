import re
from os.path import dirname, abspath
from myfuc import List, readCsv
from bs4 import BeautifulSoup as bs
from requests import get
from tryRequest import updateProxies, checkProxy, getProxy
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


def pageDl(link):
    res = get(link['url'], headers=header, proxies=getProxy(tmp))
    with open(link['filePath'], encoding='utf-8', mode='w+') as f:
        f.write(res.text)


def main1():
    updateProxies(tmp)
    checkProxy([{'proxy': proxy, 'path': tmp} for proxy in readCsv(tmp, 'proxies.csv')])
    with Pool(6) as pool:
        pool.map(pageDl, [{
            'url': f'http://www.instrument.org.tw/members/?page={i}&mode=search_list&username=有限&representative=有限&address=有限&name=有限&ch_company_name=有限&en_company_name=有限&tel_1=有限&fax=有限&project=有限&keyword=有限&u_number=有限&button=送出查詢',
            'fileName': f'{htmlPath}/list/page{i}.html'
        } for i in range(1, 43)])


def getInfo(page):
    soup = bs(open(f'{htmlPath}/list/page{page}.html', encoding='utf-8'), 'html.parser')
    return [[
        tr.select('td')[2].text,
        tr.select('td')[4].text,
        tr.select('td')[5].text,
        'http://www.instrument.org.tw/members/' + tr.select('td')[2].select('a')[0]['href'],
    ] for tr in soup.select('#main_box table tr')[1:]]


def main2():
    with Pool(6) as pool:
        results = pool.map(getInfo, [i for i in range(1, 43)])
    List([row for res in results for row in res]).writeCsv(pwd, 'orgInfo_o.csv')


def main3():
    updateProxies(tmp)
    checkProxy([{'proxy': proxy, 'path': tmp} for proxy in readCsv(tmp, 'proxies.csv')])
    with Pool(6) as pool:
        pool.map(pageDl, [{
            'url': i[3],
            'filePath': f'{htmlPath}/detail/{i[0]}.html',
        } for i in readCsv(pwd, 'orgInfo_o.csv')])


def getDetail(info):
    soup = bs(open(f'{htmlPath}/detail/{info[0]}.html', encoding='utf-8'), 'html.parser')
    tr = soup.select('#main_box table tr')
    return [
        info[0],
        tr[4].select('td')[1].text,
        info[1],
        '負責人',
        info[2],
        tr[9].select('td')[1].text,
        '臺北市儀器商業同業公會',
        '',
        tr[10].select('td')[1].text,
    ]


def main4():
    with Pool(6) as pool:
        results = pool.map(getDetail, readCsv(pwd, 'orgInfo_o.csv'))
    List(colname + results).writeCsv(pwd, 'orgInfo.csv')


if __name__ == '__main__':
    main4()
