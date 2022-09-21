import re
import logging
from os.path import dirname, abspath
from time import sleep
from myfuc import readCsv, writeCsv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from requests import get, exceptions
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
from random import uniform, choice

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


def check(proxy):
    proxy_n = {proxy[0]: f'{proxy[1]}:{proxy[2]}'}
    try:
        get('https://api.ipify.org/', proxies=proxy_n, timeout=30)
        writeCsv(f'{pwd}/.tmp', 'workProxies.csv', [proxy], mode='a+')
    except:
        pass


def checkProxy(proxies):
    pool = Pool(processes=6)
    res = pool.map(check, proxies)
    return res


def getProxy():
    proxy = choice(readCsv(f'{pwd}/.tmp', 'workProxies.csv'))[0]
    return {proxy[0]: proxy[1]}


def getLinks(driver, u):
    w = WebDriverWait(driver, 10)
    while True:
        try:
            search = w.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#KeyWord')))
            search.clear()
            search.send_keys(u)
            driver.find_element(By.CSS_SELECTOR, '.btnSearch').click()
            rows = driver.find_elements(By.CSS_SELECTOR, '#grid tbody tr')
            for row in rows:
                tds = row.find_elements(By.CSS_SELECTOR, 'td')
                res = [tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[2].find_element(By.CSS_SELECTOR, 'a').get_attribute('href')]
                writeCsv(pwd, 'links.csv', [res], mode='a+')
            driver.back()
            sleep(uniform(10, 20))
        except TimeoutException:
            driver.get('https://ulist.moe.gov.tw/Query/SimpleQuery')
            continue
        except Exception as e:
            driver.get('https://ulist.moe.gov.tw/Query/SimpleQuery')
            logging.warning(u, e)
        break


def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, filename=f'{pwd}/running.log')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://ulist.moe.gov.tw/Query/SimpleQuery')
    for u in readCsv(pwd, 'university.csv')[10:]:
        getLinks(driver, u)


class Result():
    def __init__(self, soup, link):
        self.pubpri = link[0]
        self.sys = link[1]
        self.school = link[2]
        self.link = link[3]
        self.add = []
        self.cel = []
        self.nameAdmin = soup.select('#admindata tbody tr')
        self.nameDean = soup.select('#coldata tbody tr')
        self.nameDepAdmin = soup.select('#departmentadmindata tbody tr')
        self.Dep = soup.select('#departmentdata tbody tr')
        for p in soup.select('#tabs-1 div')[0].select('p'):
            if '地址：' in p.text:
                self.add.append(p.text.replace('地址：', ''))
            elif '電話號碼：' in p.text:
                self.cel.append(p.text.replace('電話號碼：', '').replace('\r', '').replace('\n', '').replace(' ', ''))

    def getAdmin(self):
        try:
            info = [[
                self.pubpri,
                self.sys,
                self.school,
                '|'.join(self.add),
                name.select('td')[1].text,
                name.select('td')[0].text,
                name.select('td')[2].text.replace('\r', '').replace('\n', '').replace(' ', '') + '#' + name.select('td')[3].text if '無' not in name.select('td')[3].text else name.select('td')[2].text.replace('\r', '').replace('\n', '').replace(' ', ''),
                name.select('td')[5].text,
                self.link
            ] for name in self.nameAdmin]
        except IndexError:
            info = [[self.pubpri, self.sys, self.school, self.add, '', '', '', '', self.link]]
        return info

    def getDean(self):
        try:
            info = [[
                self.pubpri,
                self.sys,
                self.school,
                name.select('td')[0].text,
                '|'.join(self.add),
                name.select('td')[2].text,
                name.select('td')[1].text,
                name.select('td')[3].text.replace('\r', '').replace('\n', '').replace(' ', '') + '#' + name.select('td')[4].text if '無' not in name.select('td')[4].text else name.select('td')[3].text.replace('\r', '').replace('\n', '').replace(' ', ''),
                name.select('td')[6].text,
            ] for name in self.nameDean]
        except IndexError:
            info = [[self.pubpri, self.sys, self.school, '', self.add, '', '', '', '']]
        return info

    def getDepAdmin(self):
        try:
            info = [[
                self.pubpri,
                self.sys,
                self.school,
                name.select('td')[1].text,
                '|'.join(self.add),
                name.select('td')[3].text,
                name.select('td')[2].text,
                name.select('td')[4].text.replace('\r', '').replace('\n', '').replace(' ', '') + '#' + name.select('td')[5].text if '無' not in name.select('td')[5].text else name.select('td')[4].text.replace('\r', '').replace('\n', '').replace(' ', ''),
                name.select('td')[7].text,
            ] for name in self.nameDepAdmin]
        except IndexError:
            info = [[self.pubpri, self.sys, self.school, '', self.add, '', '', '', '']]
        return info

    def getDepInfo(self):
        try:
            info = [[
                self.pubpri,
                self.sys,
                self.school,
                name.select('td')[0].text,
                name.select('td')[1].text.replace('\n', ''),
                'https://ulist.moe.gov.tw' + name.select('td')[1].select('a')[0]['href'],
            ] for name in self.Dep]
        except IndexError:
            info = [[self.pubpri, self.sys, self.school, '', '']]
        return info


def getInfo(school):
    try:
        soup = bs(open(f'{pwd}/html/學校頁面/{school[2]}.html', encoding='utf-8'), 'html.parser')
        res = Result(soup, school)
        return [res.getAdmin(), res.getDean(), res.getDepAdmin(), res.getDepInfo()]
    except Exception as e:
        logging.warning(school[2], e)


def main3():
    schools = readCsv(pwd, 'links.csv')
    with Pool(6) as pool:
        results = pool.map(getInfo, schools)
    for i, e in enumerate(['單位主管', '學院主管', '學系主管', '學系資料']):
        writeCsv(pwd, f'{e}.csv', [row for school in results for row in school[i]], mode='w+')


def pagedl(link):
    while True:
        try:
            res = get(link['link'], headers=header, proxies=getProxy(), timeout=30)
            with open('{path}/{university}{department}.html'.format(**link), mode='w+', encoding='utf-8') as f:
                f.write(res.text)
        except (exceptions.ProxyError, exceptions.ConnectTimeout):
            continue
        except Exception as e:
            logging.warning('{university}{department}'.format(**link), e)
        break


def main2():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, filename=f'{pwd}/running.log')
    links = [{
        'university': link[2],
        'college': link[3],
        'department': link[4],
        'link': link[5],
        'path': f'{pwd}/html/系所頁面'
    } for link in readCsv(pwd, '系所_已篩選.csv')[6:]]
    with Pool(6) as pool:
        pool.map(pagedl, links)


class Teacher():
    def __init__(self, soup, department):
        self.soup = soup
        self.pubpri = department[0]
        self.sys = department[1]
        self.school = department[2]
        self.dep = department[4]
        self.site = ''
        for tr in self.soup.select('#one-column-emphasis tbody tr'):
            if '系所網址：' in tr.select('td')[0].text:
                self.site = tr.select('td')[1].text.replace('\n', '')

    def teachers(self):
        try:
            info = [[
                self.pubpri,
                self.sys,
                self.school,
                self.dep,
                name.select('td')[2].text,
                name.select('td')[1].text,
                name.select('td')[3].text,
                name.select('td')[4].text,
                self.site,
            ] for name in self.soup.select('#teacherdata tbody tr')]
        except IndexError:
            info = [[self.pubpri, self.sys, self.school, self.dep, '', '', '', '', self.site, ]]
        return info


def getTeacher(department):
    try:
        soup = bs(open(f'{pwd}/html/系所頁面/{department[2]}{department[4]}.html', encoding='utf-8'), 'html.parser')
        res = Teacher(soup, department)
        return res.teachers()
    except Exception as e:
        logging.warning(department[2], department[4], e)


def main4():
    departments = readCsv(pwd, '系所_已篩選.csv')
    with Pool(6) as pool:
        results = pool.map(getTeacher, departments)
    writeCsv(pwd, 'teachers.csv', [row for school in results for row in school], mode='w+')


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, filename=f'{pwd}/running.log')
    # updateProxies(f'{pwd}/.tmp')
    #checkProxy(readCsv(f'{pwd}/.tmp', 'proxies.csv'))
