from time import sleep
from myfuc import List, readCsv
from requests import post, get
from os.path import dirname, abspath
from bs4 import BeautifulSoup as bs
from random import uniform
from multiprocessing import Pool
from tryRequest import getProxy
import re

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
html = f'{pwd}/html'
tmp = f'{pwd}/tmp'
colname = [['公司名稱', '地址', '姓名', '職稱', '總機電話', '電子郵件信箱', '市場', '產業類別', '其他來源分類']]


def main1():
    for p in range(1, 12):
        res = get(f'https://www.tca.org.tw/searchpd.asp?page={p}',
                  cookies={'ASPSESSIONIDQWABQRQR': 'LFEDMJLCIALJHIINCMDCGHJO'},
                  headers=header)
        res.encoding = 'big5'
        open(f'{html}/page{p}.html', encoding='utf-8', mode='w+').write(res.text)
        sleep(10)


def orgList():
    res = []
    for p in range(1, 12):
        soup = bs(open(f'{html}/page{p}.html', encoding='utf-8'), 'html.parser')
        for tr in soup.select('form > table > tr')[1:]:
            res.append([tr.select('td')[0].text, tr.select('td:nth-child(2) a')[0].text, tr.select('td')[2].text])
    List(res).writeCsv(pwd, 'orgList.csv')


def getInfo(n):
    res = post('https://www.tca.org.tw/members_list.asp',
               cookies={'ASPSESSIONIDQWABQRQR': 'LPDDMJLCMIHNEGGLLJCPFKHM'},
               headers=header,
               data={'no': n},
               proxies=getProxy(tmp))
    res.encoding = 'big5'
    open(f'{html}/{n}.html', encoding='utf-8', mode='w+').write(res.text)
    sleep(uniform(3, 10))


def main2():
    # updateProxies(tmp)
    #checkProxy([{'path': tmp, 'proxy': proxy} for proxy in readCsv(tmp, 'proxies.csv')])
    with Pool(7) as pool:
        pool.map(getInfo, [n[0] for n in readCsv(pwd, 'orgList.csv')])


def main3():
    res = [['公司名稱', '地址', '姓名', '職稱', '總機電話', '電子郵件信箱', '市場', '產業類別', '其他來源分類']]
    for f in readCsv(pwd, 'orgList.csv'):
        soup = bs(open(f'{html}/{f[0]}.html', encoding='utf-8'), 'html.parser')
        tr = soup.select('.TabbedPanelsContent table tr')
        res.append([re.sub(r'（.*）', '', tr[0].select('td')[1].text), tr[1].select('td')[1].text, '', '', tr[2].select('td')[1].text, '', '臺北市電腦公會', '', tr[5].select('td')[1].text])
    List(res).writeCsv(pwd, 'orgInfo.csv')


def getJson(keyword):
    sleep(0.1)
    try:
        res = get(f'https://data.gcis.nat.gov.tw/od/data/api/6BBA2268-1367-4B42-9CCA-BC17499EBE8C?$format=json&$filter=Company_Name%20like%20{keyword[0]}%20and%20Company_Status%20eq%2001&$skip=0&$top=50').json()
        List([[r['Company_Name'], r['Company_Location'], r['Responsible_Name'], '負責人', keyword[4], keyword[5], keyword[6], keyword[7], keyword[8]] for r in res]).writeCsv(pwd, 'orgInfo_o.csv', mode='a+')
    except Exception as e:
        print(e)


def main4():
    List(colname).writeCsv(pwd, 'orgInfo_o.csv')
    for k in readCsv(pwd, 'orgInfo.csv')[1:]:
        getJson(k)


if __name__ == '__main__':
    main4()
