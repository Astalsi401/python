import codecs
import os
import sys
import multiprocessing as mp
import logging
from myfuc import readCsv, writeCsv
from csv import DictWriter
from tryRequest import *

pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'},
    {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'},
]
fail = 0


def m1(kind):
    page = 1
    while True:
        logging.info(f'kind: {kind}, page: {page}')
        soup = request(f'https://eatender.firdi.org.tw/product/list?type=t1&kind={kind}&page={page}')
        food = soup.select('#icons-01 a.food-inner')
        if food == []:
            break
        for a in food:
            writeCsv(f'{pwd}/csv', 'eatender.csv', [[a['href'], ]], mode='a+')
        page += 1


def pre():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    updateProxies(f'{pwd}/.tmp', 'proxies.csv')


def main1():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    writeCsv(f'{pwd}/csv', 'eatender.csv', [])
    process_list = []
    for kind in ['主食', '主菜', '配菜', '湯品', '點心', '飲品', '乳品', '休閒食品', '調味品', 'RTC食材', '餐食', '其他']:
        process_list.append(mp.Process(target=m1, args=(kind,)))
    for p in process_list:
        p.start()
    for p in process_list:
        p.join()


def m2(url):
    soup = request(url)
    rows = soup.select('table.table-detail')[0].find_all('tr')
    data = {'產品頁面': url}
    for r in rows:
        name = r.select('td')[0]
        info = r.select('td')[1]
        if name.text in ['產品名稱', '公司', '產品類別', '公司官網']:
            data[name.text] = info.text.replace('\n', '').replace(' ', '')
        elif name.text == '銷售通路':
            data[name.text] = [li.text.replace('\n', '').replace(' ', '') for li in info.select('li')]
    with open(f'{pwd}/csv/foodinfo.csv', mode='a+', newline='', encoding='utf-8-sig') as f:
        writer = DictWriter(f, fieldnames=['產品名稱', '公司', '產品類別', '銷售通路', '公司官網', '產品頁面'])
        writer.writerow(data)
    return data


def main2():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    writeCsv(f'{pwd}/csv', 'foodinfo.csv', [])
    pool = mp.Pool(processes=6)
    res_list = []
    for url in readCsv(f'{pwd}/csv', 'eatender.csv'):
        res_list.append(pool.apply_async(m2, (url[0],)))
    for res in res_list:
        print(res.get())


if __name__ == '__main__':
    pre()
