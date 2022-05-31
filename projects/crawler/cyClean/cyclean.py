import os
from random import randint
from myfuc import writeCsv, readCsv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
options = Options()


def getUrls():
    url = 'http://www.cy-clean.com/%E9%80%9A%E9%81%8E%E7%94%A2%E5%93%81%E5%8F%8A%E5%BB%A0%E5%95%86/'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    writeCsv(f'{pwd}/csv', 'results.csv', [])
    for p in range(2, 21):
        lists = driver.find_elements(By.CSS_SELECTOR, '#newsPanelResults div.afs-Loadingdata')
        for a in lists:
            row = []
            row.append(a.find_element(By.CSS_SELECTOR, 'h4').text)
            for b in a.find_elements(By.CSS_SELECTOR, '.prDateCol'):
                row.append(b.text)
            row.append(a.find_element(By.CSS_SELECTOR, 'h4 a[href]').get_attribute('href'))
            writeCsv(f'{pwd}/csv', 'results.csv', [row], mode='a+')
        if p <= 19:
            sleepTime = randint(20, 30)
            print(f'go to page {p}')
            page = len(driver.find_elements(By.CSS_SELECTOR, '.pagination li')) - 1
            driver.find_elements(By.CSS_SELECTOR, f'.pagination li')[page].find_element(By.CSS_SELECTOR, 'a').click()
            for a in range(0, sleepTime):
                print(f'wait {sleepTime - a} sec')
                sleep(1)


def getData():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    writeCsv(f'{pwd}/csv', 'results2.csv', [[
        '經營業者名稱',
        '負責人',
        '證書字號',
        '所在地',
        '電話',
        '評鑑有效日期',
        '通過產品數',
        '通過評鑑日期',
        '標準',
        '產品名稱'
    ]])
    links = readCsv(f'{pwd}/csv', 'results.csv')
    left = len(links)
    for a in links:
        driver.get(a[len(a) - 1])
        sleepTime = randint(10, 30)
        for b in range(sleepTime, 0, -1):
            sleep(1)
            print(f'wait {b} sec')
        basic = driver.find_element(By.CSS_SELECTOR, '#gc_company_table_basic')
        items = driver.find_element(By.CSS_SELECTOR, '#gc_company_table_items')
        rowBasic = [b.text for b in basic.find_elements(By.CSS_SELECTOR, '.gc_column_content')]
        rowItems = [b.text for b in items.find_elements(By.CSS_SELECTOR, '.gc_column_content')]
        rowItems = [rowItems[b:b + 3] for b in range(0, len(rowItems), 3)]
        for b in rowItems:
            row = [a[0], a[1], a[2], a[3], rowBasic[3], rowBasic[4], rowBasic[6]]
            row.extend(b)
            writeCsv(f'{pwd}/csv', 'results2.csv', [row], mode='a+')
        left -= 1
        print(f'{left} page left')


def main():
    getData()


if __name__ == '__main__':
    main()
