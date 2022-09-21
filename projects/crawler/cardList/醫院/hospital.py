import re
import logging
from os.path import dirname, abspath
from random import uniform, choice
from time import sleep
from requests import get, exceptions
from myfuc import readCsv, writeCsv, List
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
chop = Options()
chop.add_extension(f'{pwd}/extensions/adblock_4.46.2_0.crx')


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


def getLinks():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://mcia.mohw.gov.tw/openinfo/A100/A101-1.aspx')
    w = WebDriverWait(driver, 20)
    submit = w.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_btSEARCH')))
    level = Select(driver.find_element(By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_ddlCONTRIBUTING_KIND'))
    cat = '醫學中心'
    level.select_by_visible_text(cat)
    submit.click()
    page = 12
    while True:
        sleep(15)
        res = w.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_gviewMain')))
        for row in res.find_elements(By.CSS_SELECTOR, 'tr')[1:21]:
            org = row.find_elements(By.CSS_SELECTOR, 'td')[0].text
            link = row.find_elements(By.CSS_SELECTOR, 'td')[4].find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            writeCsv(pwd, 'hospital.csv', [[org, link, cat]], 'a+')
        try:
            page += 1
            if page == 11:
                driver.find_element(
                    By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table/tbody/tr[2]/td/div/table/tbody/tr[22]/td/table/tbody/tr/td[11]/a').click()
            else:
                driver.find_element(By.XPATH, f'//a[contains(text(), "{page}")]').click()
            continue
        except NoSuchElementException:
            break
        except Exception as e:
            print(e)


def getInfo(url):
    while True:
        try:
            res = get(url[1], headers=header, proxies=getProxy(), timeout=30)
        except (exceptions.ProxyError, exceptions.ConnectTimeout):
            continue
        except Exception as e:
            logging.warning(url, e)
        break
    soup = bs(res.text, 'lxml')
    org = soup.select('#ctl00_ContentPlaceHolder1_lbBAS_NAME')[0].text
    loc = soup.select('#ctl00_ContentPlaceHolder1_lbZONE_ADDR')[0].text
    name = soup.select('#ctl00_ContentPlaceHolder1_lbBAS_HAD_NAME')[0].text
    cel = soup.select('#ctl00_ContentPlaceHolder1_lbBAS_TEL_NO')[0].text
    sleep(uniform(2, 5))
    writeCsv(pwd, 'orgInfo_c.csv', [[org, loc, name, '院長', cel, '', url[2]]], 'a+')
    return [org, loc, name, '院長', cel, '', url[2]]


def main():
    links = readCsv(pwd, 'hospital-c.csv')
    with Pool(6) as pool:
        res = pool.map(getInfo, links)
    return res


def appendCsv():
    a = readCsv(pwd, 'orgInfo_n2.csv')
    b = readCsv(pwd, 'orgInfo_c2.csv')
    List(a + b).writeCsv(pwd, 'hospital-all.csv')


if __name__ == '__main__':
    # updateProxies(f'{pwd}/.tmp')
    #checkProxy(readCsv(f'{pwd}/.tmp', 'proxies.csv'))
    #writeCsv(pwd, 'orgInfo_c2.csv', main(), 'w+')
    appendCsv()
