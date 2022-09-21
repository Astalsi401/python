import re
from os.path import dirname, abspath
from requests import get
from bs4 import BeautifulSoup as bs
from myfuc import writeCsv

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}


def tsrm():
    res = get('http://www.tsrm.org.tw/agency/', headers=header)
    res.encoding = 'utf-8'
    soup = bs(res.text, 'lxml')
    writeCsv(pwd, 'orgInfo-tsrm.csv', [[row.select('td')[0].text, row.select('td')[1].text, '', '', row.select('td')[2].text, '', '國民健康署許可通過人工生殖機構'] for row in soup.select('.list')[0].select('tbody tr')])


def jct():
    res = get('https://www.jct.org.tw/cp-1261-7543-e0858-1.html', headers=header)
    res.encoding = 'utf-8'
    soup = bs(res.text, 'lxml')
    writeCsv(pwd, 'orgInfo-jct.csv', [[row.select('td')[1].select('div')[0].text, '診所美容醫學品質認證通過之醫療機構'] for row in soup.select('.cp table tbody')[1].select('tr') if row.select('td')[2].select('div')[0].text in ['臺北市', '新北市', '基隆市', '新竹市', '桃園市', '新竹縣', '宜蘭縣']])


jct()
