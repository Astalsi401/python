import re
from os.path import dirname, abspath
from bs4 import BeautifulSoup as bs
from myfuc import List, readCsv
from tryRequest import pageDl, updateProxies, checkProxy
from multiprocessing import Pool


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


def getLinks():
    soup = bs(open(f'{html}/teeia.html', encoding='utf-8'), 'html.parser')
    List([[li.select('h4')[0].text.replace(' ', ''), li.select('a')[0]['href'].replace(' ', '')] for li in soup.select('.facturer_list li')]).writeCsv(pwd, 'orgLinks.csv')


def main():
    # updateProxies(tmp)
    #checkProxy([{'proxy': proxy, 'path': tmp} for proxy in readCsv(tmp, 'proxies.csv')])
    with Pool(6) as pool:
        pool.map(pageDl, [{'url': link[1], 'filePath': f'{html}/{link[0]}.html', 'proxyPath': tmp} for link in readCsv(pwd, 'orgLinks.csv')])


def getInfo(link):
    soup = bs(open(f'{html}/{link[0]}.html', encoding='utf-8'), 'html.parser')
    res = {
        '企業中文名稱': '',
        '聯絡地址': '',
        '董事長': '',
        '聯絡電話': '',
        '電子郵件': '',
    }
    for li in soup.select('.ul_table_content li'):
        res[li.select('div.ul_table_name p')[0].text] = li.select('div._ul_note')[0].text.replace('\n', '').replace(' ', '').replace('‧', '、')
    return [res['企業中文名稱'], res['聯絡地址'], res['董事長'], '董事長', res['聯絡電話'], res['電子郵件'], '臺灣電子設備協會名單', '']


def main1():
    with Pool(6) as pool:
        results = pool.map(getInfo, readCsv(pwd, 'orgLinks.csv'))
    List(colname + results).writeCsv(pwd, 'orgInfo.csv')


if __name__ == '__main__':
    main1()
