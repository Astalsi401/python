import re
from os.path import dirname, abspath
from bs4 import BeautifulSoup as bs
from myfuc import List
from requests import get

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


def dl():
    res = get('https://rank.twincn.com/rank.aspx?code=%E5%89%B5%E6%A5%AD%E6%8A%95%E8%B3%87%E5%85%AC%E5%8F%B8(649914)', headers=header)
    with open(f'{html}/清單.html', encoding='utf-8', mode='w+') as f:
        f.write(res.text)


def getLinks():
    soup = bs(open(f'{html}/清單.html', encoding='utf-8'), 'html.parser')
    List(colname + [[
        tr.select('td:nth-child(2) a')[0].text,
        '',
        '',
        '',
        '',
        '',
        '創投'
        '',
        '',
    ] for tr in soup.select('.table.table-striped tbody tr') if len(tr.select('td')) == 3]).writeCsv(pwd, 'orgInfo.csv')


if __name__ == '__main__':
    getLinks()
