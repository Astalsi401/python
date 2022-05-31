import codecs
import os
import requests
import sys
from bs4 import BeautifulSoup
from csv import writer, reader
from random import uniform, randint
from time import sleep

pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/').replace('/py', '')
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
}
fail = 0


def writeCsv(data, name, mode):
    if not os.path.isdir(f'{pwd}/csv/getCategory'):
        os.makedirs(f'{pwd}/csv/getCategory')
    with open(f'{pwd}/csv/getCategory/{name}.csv', mode=f'{mode}', encoding='utf-8-sig', newline='') as f:
        for a in data:
            writer(f).writerow(a)
    print(f'{name}.csv saved!')


def readCsv(name):
    a = []
    with open(f'{pwd}/csv/getCategory/{name}.csv', mode='r', encoding='utf-8-sig', newline='') as f:
        b = reader(f)
        for c in b:
            a.append(c)
    return a


def upDateProxies():
    res = requests.get('https://www.us-proxy.org/', headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml').select('#list tbody tr')
    a = []
    for b in soup:
        c = []
        d = 0
        for e in b.select('td'):
            if d == 0 or d == 1 or d == 6:
                c.append(e.text.replace('yes', 'https').replace('no', 'http'))
            d += 1
        a.append(c)
    writeCsv(a, 'proxies', 'w+')


def getProxy():
    proxies = readCsv('proxies')
    a = randint(0, len(proxies) - 1)
    proxy = {
        f'{proxies[a][2]}': f'http://{proxies[a][0]}:{proxies[a][1]}',
    }
    return proxy


def request(url, fail=fail):
    limit = 1
    while True:
        sleepSec = uniform(20, 30)
        try:
            proxy = getProxy()
            res = requests.get(url, headers=headers, proxies=proxy)
            res.encoding = 'utf-8'
            print(f'{proxy}\r\nrequest successful, sleep {sleepSec} sec\r\nlimit:{limit}\r\nfail:{fail}')
            sleep(sleepSec)
        except:
            if limit >= 15:
                print('retry limit: 10')
                break
            if fail > 5:
                upDateProxies()
                fail = 0
            limit += 1
            fail += 1
            print(f'{proxy}\r\nrequest fail, retry in {sleepSec} sec...\r\nlimit:{limit}\r\nfail:{fail}')
            sleep(sleepSec)
            print(f'start retry')
            continue
        break
    return BeautifulSoup(res.text, 'lxml')


def getFields1(soup):
    data = []
    fields = soup.select('div.sc-wfit35-0.sc-6qd6g7-6.dJzMTK li.iCFbap')
    for a in fields:
        for b in a.select('a'):
            data.append([a.find('span').text, b.text, b['href']])
    return data


def getFields2(soup, a, b):
    fields = soup.select('div#category-group a')
    for c in fields:
        a.append([b[0], b[1], c.text, c['href']])
        print(f'get {a[len(a) - 1]}')


def getFields3(soup, a, b):
    for c in soup:
        for d in c.select('li.clearfix'):
            if c.find('h2').text != None or d.find('span').text.replace('\n', '').replace(' ', '') != None:
                a.append([b[0], b[1], b[2], c.find('h2').text, d.find('span').text.replace('\n', '').replace(' ', '')])
            else:
                a.append([b[0], b[1], b[2], None, None])
            print(f'get {a[len(a) - 1]}')


def phase1():
    soup = request('https://www.medicalexpo.com')
    data = getFields1(soup)
    writeCsv(data, 'fields1', 'w+')


def phase2():
    data = readCsv('fields1')
    a = []
    for b in data:
        soup = request(b[2])
        getFields2(soup, a, b)
    writeCsv(a, 'fields2', 'a+')


def phase3():
    data = readCsv('fields2')
    writeCsv([], 'fields3', 'w+')
    for b in data:
        a = []
        soup = request(b[3]).select('form#floatbar li.dropdown')
        getFields3(soup, a, b)
        writeCsv(a, 'fields3', 'a+')


def main():
    # phase1()
    # phase2()
    phase3()


if __name__ == '__main__':
    main()
