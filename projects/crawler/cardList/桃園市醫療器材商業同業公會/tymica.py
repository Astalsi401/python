import re
from os.path import dirname, abspath
from myfuc import List
from bs4 import BeautifulSoup as bs
from requests import get

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
htmlFile = f'{pwd}/html/tymica.html'
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


def pageDl():
    res = get('http://www.tymica.org.tw/guild')
    with open(htmlFile, encoding='utf-8', mode='w+') as f:
        f.write(res.text)


def main():
    soup = bs(open(htmlFile, encoding='utf-8'), 'html.parser')
    trs = soup.select('.table tbody tr')
    rows = []
    for tr in trs:
        td = tr.select('td')
        if '會員編號' not in td[0].text:
            rows.append({
                'contact': td[1].text.replace('\t', ''),
                'name': td[2].text,
                'cate': td[3].text.replace('\t', '').replace('☆', '').replace('。', '').split('\n'),
            })
    List(colname + [[
        row['contact'].split('\n')[0],
        row['contact'].split('\n')[1],
        row['name'],
        '',
        re.search(r'Tel：\S+', row['contact']).group().replace('Tel：', ''),
        re.search(r'\S+@\S+', row['contact']).group().replace('信箱:', '') if re.search(r'\S+@\S+', row['contact']) else '',
        '桃園市醫療器材商業同業公會',
        '',
        '、'.join(row['cate']),
    ] for row in rows]).writeCsv(pwd, 'orgInfo.csv')


if __name__ == '__main__':
    main()
