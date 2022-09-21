import re
from os.path import dirname, abspath
from myfuc import writeCsv, List
from bs4 import BeautifulSoup as bs

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
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


def main():
    soup = bs(open(f'{pwd}/html/xtmica.html', encoding='utf-8'), 'html.parser')
    List(colname + [[
        tr.select('td')[1].text.replace('\n', ''),
        tr.select('td')[4].text.replace('\n', ''),
        tr.select('td')[3].text.replace('\n', ''),
        '',
        tr.select('td')[5].text.replace('\n', ''),
        '',
        '新北市醫療器材商業同業公會',
        '',
        tr.select('td')[2].text.replace('\n', ''),
    ] for tr in soup.select('tbody tr')[:-1]]).writeCsv(pwd, 'orgInfo.csv')


if __name__ == '__main__':
    main()
