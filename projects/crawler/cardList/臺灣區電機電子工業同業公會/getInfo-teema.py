import re
from myfuc import List, readCsv
from requests import get
from os.path import dirname, abspath
from bs4 import BeautifulSoup as bs
from time import sleep

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
html = f'{pwd}/html'


def getList():
    res = get(f'http://www.teemab2b.com.tw/NewProductList.aspx?product=醫療')
    res.encoding = 'utf-8'
    open(f'{html}/orgList.html', encoding='utf-8', mode='w+').write(res.text)


def getList2():
    soup = bs(open(f'{html}/orgList.html', encoding='utf-8'), 'html.parser')
    List([[tr.select('td:nth-child(2) a')[0].text, tr.select('td:nth-child(2) a')[0]['href']] for tr in soup.select('table#tblCompanyList tr')[1:]]).writeCsv(pwd, 'orgList.csv')


def getInfo():
    for url in readCsv(pwd, 'orgList.csv'):
        res = get(f'http://www.teemab2b.com.tw/{url[1]}')
        res.encoding = 'utf-8'
        open(f'{html}/{url[0]}.html', encoding='utf-8', mode='w+').write(res.text)
        sleep(10)


def getInfo2():
    res = [['公司名稱', '地址', '姓名', '職稱', '總機電話', '電子郵件信箱', '市場', '產業類別', '其他來源分類']]
    for c in readCsv(pwd, 'orgList.csv'):
        soup = bs(open(f'{html}/{c[0]}.html'), 'html.parser')
        tr_l = soup.select('#divMain table')[0].select('tr')
        tr_r = soup.select('#divMain table')[1].select('tr')
        res.append([
            tr_l[1].select('td')[0].text.replace('\n', ''),
            tr_r[4].select('td')[0].text.replace('\n', ''),
            tr_l[4].select('td')[0].text.replace('\n', ''),
            '負責人',
            tr_r[2].select('td')[0].text.replace('\n', ''),
            tr_l[6].select('td')[0].text.replace('\n', ''),
            '臺灣區電機電子工業同業公會', '', '', ])
    List(res).writeCsv(pwd, 'orgInfo.csv')


if __name__ == '__main__':
    getInfo2()
