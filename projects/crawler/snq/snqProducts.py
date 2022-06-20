from bs4 import BeautifulSoup
from csv import writer, reader
from requests import get
from os import makedirs
from os.path import dirname, abspath, isdir
from myfuc import readCsv, writeCsv
from time import sleep

pwd = dirname(abspath(__file__))


def writeCsv(path, name, data, mode='w+', enc='utf-8-sig'):
    '''list to csv'''
    if not isdir(path):
        makedirs(path)
    with open(f'{path}/{name}', mode=mode, encoding=enc, newline='') as f:
        for a in data:
            writer(f).writerow(a)
    print(f'{name} saved!')


def readCsv(path, name, enc='utf-8-sig'):
    '''csv to list'''
    with open(f'{path}/{name}', mode='r', encoding=enc, newline='') as f:
        return [a for a in reader(f)]


def getLinks():
    res = get('https://www.snq.org.tw/chinese/02_products/list.php')
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml').select('.SubmenuText ul li a')
    links = [[a.text, a['href'].replace('list.php?', '')] for a in soup]
    writeCsv(f'{pwd}/csv', 'links.csv', links)
    return links


def getProducts():
    writeCsv(f'{pwd}/csv', 'products.csv', [], mode='w+')
    for link in readCsv(f'{pwd}/csv', 'links.csv'):
        print(link)
        page = 320
        while True:
            url = f'https://www.snq.org.tw/chinese/02_products/list.php?page={page}&{link[1]}'
            print(url)
            res = get(url)
            res.encoding = 'utf-8'
            prods = BeautifulSoup(res.text, 'lxml').select('.prolist-down ul a')
            sleep(5)
            if prods:
                for p in prods:
                    row = [link[0], p.find('h3').text, p['href']]
                    print(row)
                    writeCsv(f'{pwd}/csv', 'products.csv', [row], mode='a+')
                    page += 16
            else:
                print('目前暫無資料')
                break


def main():
    # getLinks()
    getProducts()


main()
