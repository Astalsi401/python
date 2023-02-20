from os import chdir
from os.path import dirname, abspath, isfile
from requests import get, post
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
from time import sleep
from myfuc import List, readCsv
from tryRequest import checkProxy, updateProxies, pageDl
import pandas as pd
import re

chdir(dirname(abspath(__file__)))
pName = '產品名稱'
oName = '公司名稱'
source = '通過標章'
oTel = '公司電話'
oAdd = '公司地址'
link = 'link'
expCol = [pName, oName, source, oTel, oAdd, link]
excel = 'excel'
tmp = '.tmp'
html = 'html'


def findStr(soup, reg):
    rep = r'(Number|Star|Valid Date\.|Name|Tel|Email|FB|Website)'
    return re.sub(f'{rep}$', '', '、'.join([re.sub(f'^{rep}：', '', m.group(0)) for m in re.compile(f'{reg}[^：]+').finditer(soup.text)]))


def addCol(df):
    for col in expCol:
        if col not in df.columns:
            df[col] = ''
    return df


def fda():
    df = pd.read_excel(f'{excel}/健康食品認證通過名單.xlsx', usecols=['許可證字號', '中文品名', '申請商'], engine='openpyxl')
    df = df.rename(columns={'中文品名': pName, '申請商': oName})
    df[source] = '健康食品認證通過名單'
    addCol(df)[expCol].to_csv(f'{excel}/results_fda.csv', index=False)


def aa_getUrls():
    soup = bs(open('html/無添加網絡.htm', mode='r'), 'html.parser').select('.summary-title a')
    List([['公司名稱', 'URL']]).writeCsv(f'{excel}/urls_aa.csv', mode='w+')
    List([[re.sub(r'^\s|\s$|\n', '', a.text), a['href']] for a in soup]).writeCsv(f'{excel}/urls_aa.csv', mode='a+')


def aa_getContent():
    urls = readCsv(f'{excel}', 'urls_aa.csv')[1:]
    csv = f'{excel}/results_aa.csv'
    List([expCol]).writeCsv(csv, mode='w+')
    for name, url in urls:
        name = re.sub(r"\/|\?", "", name)
        soup = bs(open(f'{html}/無添加/{name}.html'), 'html.parser').select('div.sqs-block-content')
        soup = [w for w in soup if [m.group(0) for m in re.compile('Certificate Info').finditer(w.text)] != []]
        soup = soup[0] if len(soup) != 0 else None
        if soup:
            product = findStr(soup, r'Name：')
            tel = findStr(soup, r'Tel：')
            List([[product, name, 'AA無添加協會', tel, '', url]]).writeCsv(csv, mode='a+')


def tseYue():
    for i in range(1, 21):
        if isfile(f'{html}/慈悅/page{i}.html'):
            continue
        res = post('http://www.cy-clean.com/wp-admin/admin-ajax.php', data={
            'action': 'my_action',
            'filingType': '',
            'filterBy': '',
            'filterMonths': '',
            'filterYears': '',
            'withPDF': 'false',
            'page': f'{i}',
        })
        open(f'{html}/慈悅/page{i}.html', mode='w+').write(res.text)
        sleep(15)


def tseYue_urls():
    List([]).writeCsv(f'{excel}/urls_tseYue.csv', mode='w+')
    for i in range(1, 21):
        soup = bs(open(f'{html}/慈悅/page{i}.html', mode='r'), 'html.parser').select('div.afs-Loadingdata')
        List([[a.select('h4')[0].text, a.select('h4 a')[0]['href']] for a in soup]).writeCsv(f'{excel}/urls_tseYue.csv', mode='a+')


def tseYue_content():
    List([expCol]).writeCsv(f'{excel}/results_tseYue.csv', mode='w+')
    for name, url in readCsv(excel, 'urls_tseYue.csv'):
        soup = bs(open(f'{html}/慈悅/{name}.html', mode='r'), 'html.parser')
        add = soup.select('#gc_company_table_basic > div.gc_row:nth-child(4) .gc_column_content')[0].text
        tel = soup.select('#gc_company_table_basic > div.gc_row:nth-child(6) .gc_column_content.left')[0].text
        product = soup.select('#gc_company_table_items > div.gc_row:nth-child(3) > div.gc_column_content:nth-child(2)')[0].text
        List([[product, name, '潔淨標章', tel, add, url]]).writeCsv(f'{excel}/results_tseYue.csv', mode='a+')


def eatender():
    for i in range(1, 15):
        res = get(f'https://eatender.firdi.org.tw/award?year=2022&page={i}').text
        open(f'{html}/銀髮/page{i}.html', mode='w+').write(res)
        sleep(15)


def eatender_urls():
    List([]).writeCsv(f'{excel}/urls_eatender.csv', mode='w+')
    for i in range(1, 15):
        soup = bs(open(f'{html}/銀髮/page{i}.html', mode='r'), 'html.parser').select('div.line-warp:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a')
        List([[re.sub(r'\n|\s', '', a.text), a['href']] for a in soup]).writeCsv(f'{excel}/urls_eatender.csv', mode='a+')


def eatender_content():
    file = f'{excel}/results_eatender.csv'
    List([expCol]).writeCsv(file, mode='w+')
    for product, url in readCsv(excel, 'urls_eatender.csv'):
        product = re.sub(r'\/|\?|\|', '', product)
        tr = bs(open(f'{html}/銀髮/{product}.html', mode='r'), 'html.parser').select('.table-detail tr')
        List([[product, tr[1].text, '銀髮友善食品', '', '', url]]).writeCsv(file, mode='a+')


def main():
    #writer = pd.ExcelWriter(f'{excel}/results.xlsx', engine='xlsxwriter')
    # writer.close()
    df = fda()
    #df = aa()
    addCol(df).to_csv(f'{excel}/results_fda.csv', index=False)


def main1():
    # updateProxies(tmp)
    #checkProxy([{'path': tmp, 'proxy': proxy} for proxy in readCsv(tmp, 'proxies.csv')])
    urls = readCsv(excel, 'urls_eatender.csv')
    urls = [[re.sub(r'\/|\?|\|', '', name), url] for name, url in urls if isfile(f'{html}/銀髮/{name}.html') == False]
    with Pool(8) as pool:
        pool.map(pageDl, [{'url': url, 'filePath': f'{html}/銀髮/{name}.html', 'proxyPath': tmp} for name, url in urls])


def main2():
    df = pd.concat([pd.read_csv(f'{excel}/results_{w}.csv') for w in ['aa', 'eatender', 'fda', 'tseYue']])
    df.to_excel(f'{excel}/results.xlsx', index=False)


if __name__ == '__main__':
    main2()
