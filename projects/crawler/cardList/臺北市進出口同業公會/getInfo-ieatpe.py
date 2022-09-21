import re
import logging
from os.path import dirname, abspath
from time import sleep
from tkinter.tix import Select
from myfuc import readCsv, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
colname = [[
    '公司名稱',
    '住址',
    '姓名',
    '職稱',
    '總機電話',
    '電子郵件信箱',
    '市場',
    '產業類別',
    '其他來源分類'
]]


def getContents(driver):
    for corp in driver.find_elements(By.CSS_SELECTOR, '#tbMain > tbody:nth-child(2) > tr'):
        while True:
            corp.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > a').click()
            sleep(5)
            if driver.find_element(By.CSS_SELECTOR, '#btnConfirm').is_displayed():
                break
            else:
                continue
        logging.info('Click Company')
        row = [
            driver.find_element(By.CSS_SELECTOR, '#detlModal span[data-name="Cname"]').text,
            driver.find_element(By.CSS_SELECTOR, '#detlModal p[data-name="Caddr"]').text,
            driver.find_element(By.CSS_SELECTOR, '#detlModal p[data-name="Cowner"]').text,
            driver.find_element(By.CSS_SELECTOR, '#detlModal p[data-name="tel"]').text,
            driver.find_element(By.CSS_SELECTOR, '#detlModal a[data-name="email"]').text,
            driver.find_element(By.CSS_SELECTOR, '#detlModal a[data-name="url"]').text
        ]
        List([row]).writeCsv(pwd, 'orgInfo_o.csv', mode='a+')
        sleep(2)
        w = WebDriverWait(driver, 10)
        confirm = w.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#btnConfirm')))
        confirm.click()
        sleep(1)


def getLinks():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.ieatpe.org.tw/qry/query.aspx?utm_campaign=header')
    driver.find_elements(By.CSS_SELECTOR, '#tabtp li')[1].click()
    driver.find_element(By.CSS_SELECTOR, '#ptype > div:nth-child(1) > label:nth-child(2)').click()
    sleep(3)
    cat = Select(driver.find_element(By.CSS_SELECTOR, '#ddlPtype'))
    cat.select_by_value('30')
    driver.find_element(By.CSS_SELECTOR, '#ptype > div:nth-child(2) > span:nth-child(2)').click()
    sleep(3)
    prodsPage = driver.find_elements(By.CSS_SELECTOR, '#tbSub_paginate > span:nth-child(3) > a')
    for i in range(1, len(prodsPage)):
        driver.find_elements(By.CSS_SELECTOR, '#tbSub_paginate > span:nth-child(3) > a')[i].click()
        logging.info(f'Click Prods Page: {i+1}')
        sleep(1)
        for tr in driver.find_elements(By.CSS_SELECTOR, '#tbSub tbody tr')[4:]:
            sleep(2)
            tr.find_element(By.CSS_SELECTOR, 'td:nth-child(1) a').click()
            logging.info('Click Hs Code')
            sleep(1)
            for j in range(0, len(driver.find_elements(By.CSS_SELECTOR, 'div.dataTables_paginate:nth-child(2) > select:nth-child(2) > option'))):
                page = Select(driver.find_element(By.CSS_SELECTOR, '#tbMain_paginate select'))
                page.select_by_index(j)
                logging.info(f'Click Corps Page: {j+1}')
                getContents(driver)


def fm():
    List(colname + [[row[0], row[1], row[2], '', row[3], row[4], '臺北市進出口同業公會', '', ''] for row in readCsv(pwd, 'orgInfo_o.csv')]).writeCsv(pwd, 'orgInfo.csv')


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, filename=f'{pwd}/running.log')
    # getLinks()
    fm()
