import re
from os.path import dirname, abspath
from random import uniform, choice
from time import sleep
from requests import get, exceptions
from myfuc import readCsv, writeCsv
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
import logging

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}


def updateProxies(path):
    writeCsv(path, 'proxies.csv', [], mode='w+')
    res = get('https://www.sslproxies.org/', headers=header)
    res.encoding = 'utf-8'
    proxies_list = bs(res.text, 'lxml').select('#list tbody tr')
    for row in proxies_list:
        proxy = row.select('td')
        writeCsv(path, 'proxies.csv', [['https', proxy[0].text, proxy[1].text]], mode='a+')


def check_n(proxy):
    proxy_n = {proxy[0]: f'{proxy[1]}:{proxy[2]}'}
    try:
        get('https://api.ipify.org/', proxies=proxy_n, timeout=30)
        writeCsv(f'{pwd}/.tmp', 'workProxies.csv', [proxy], mode='a+')
    except:
        pass


def checkProxy(proxies):
    pool = Pool(processes=6)
    res = pool.map(check_n, proxies)
    return res


def getProxy():
    proxy = choice(readCsv(f'{pwd}/.tmp', 'workProxies.csv'))[0]
    return {proxy[0]: proxy[1]}


def getLists():
    writeCsv(pwd, 'orgs.csv', [], 'w+')
    for p in range(1, 52):
        res = get(f'https://sme.moeasmea.gov.tw/startup/modules/rmap/creative_space_list.php?city=&page={p}', headers=header)
        soup = bs(res.text, 'lxml')
        orgs = soup.select('.card-list-content h3 a')
        for org in orgs:
            row = ['https://sme.moeasmea.gov.tw/startup/modules/rmap/' + org.get('href'), org.getText()]
            print(row)
            writeCsv(pwd, 'orgs.csv', [row], 'a+')
        sleep(uniform(15, 30))


def getInfo(url):
    while True:
        try:
            res = get(url, headers=header, proxies=getProxy(), timeout=30)
        except (exceptions.ProxyError, exceptions.ConnectTimeout):
            continue
        except Exception as e:
            logging.warning(url, e)
        break
    soup = bs(res.text, 'lxml')
    orgs = soup.select('.placr_details_infor')[0]
    info = orgs.select('ul')[2].select('li')
    reg = re.compile(r'(?<=：)[\s\S]*')
    row = [
        '',
        orgs.select('h1')[0].text,
        reg.findall(info[0].text)[0],
        '',
        '',
        reg.findall(info[1].text)[0],
        reg.findall(info[2].text)[0],
        reg.findall(info[3].text)[0],
        ''
    ]
    writeCsv(pwd, 'orgsInfo_n.csv', [row], 'a+')
    sleep(uniform(2, 5))


def main():
    logging.basicConfig(filename=f'{pwd}/.tmp/info.log', filemode='a+', format='%(levelname)s:%(message)s', level=logging.INFO)
    urls = [url[0] for url in readCsv(pwd, 'orgs.csv')]
    with Pool(6) as pool:
        res = pool.map(getInfo, urls)
    return res


if __name__ == '__main__':
    # updateProxies(f'{pwd}/.tmp')
    #checkProxy(readCsv(f'{pwd}/.tmp', 'proxies.csv'))
    main()

# getInfo()
