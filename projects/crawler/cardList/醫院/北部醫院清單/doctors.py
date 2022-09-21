import re
from time import sleep
from requests import get
from os.path import dirname, abspath
from bs4 import BeautifulSoup as bs
from myfuc import List, readCsv
from tryRequest import updateProxies, checkProxy, pageDl
from multiprocessing import Pool

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
html = f'{pwd}/html'
tmp = f'{pwd}/tmp'

hospital = [
    ['https://wwwv.tsgh.ndmctsgh.edu.tw/doctable/191/26398', '三軍總醫院'],
]


def dl1(url):
    sleep(0.5)
    res = get(url[0])
    open(f'{html}/{url[1]}.html', encoding='utf-8', mode='w+').write(res.text)


def info1():
    soup = bs(open(f'{html}/三軍總醫院.html', encoding='utf-8'), 'html.parser')
    res = [[
        f"https://wwwv.tsgh.ndmctsgh.edu.tw{a['href']}",
        a['title']
    ] for i in range(2, 7) for a in soup.select(f'div.col-xs-12:nth-child({i}) > div:nth-child(2) > div > a')]
    List(res).writeCsv(pwd, 'links.csv')


def doctorsLinks():
    for a in readCsv(pwd, 'links.csv'):
        dl1([a[0], f'三軍總醫院-{a[1]}'])


def doctors():
    res = []
    for link in readCsv(pwd, 'links.csv'):
        soup = bs(open(f'{html}/三軍總醫院-{link[1]}.html', encoding='utf-8'), 'html.parser')
        res += [[f'https://wwwv.tsgh.ndmctsgh.edu.tw{a["href"]}', f'三軍總醫院-{a["title"]}'] for a in soup.select('.column.column-block.lg-txt > a')]
    List(res).writeCsv(pwd, 'doctorLinks.csv')


def doctorsInfoDl():
    # updateProxies(tmp)
    #checkProxy([{'path': tmp, 'proxy': proxy} for proxy in readCsv(tmp, 'proxies.csv')])
    with Pool(6) as pool:
        pool.map(pageDl, [{'url': link[0], 'filePath': f'{html}/{link[1]}.html', 'proxyPath': tmp} for link in readCsv(pwd, 'doctorLinks.csv')])


def doctorInfo(file):
    soup = bs(open(f'{html}/{file[1]}.html', encoding='utf-8'), 'html.parser')
    name = soup.select('h2[style="color: blue;"]')[0].text


if __name__ == "__main__":
    doctorsInfoDl()
