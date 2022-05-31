import os
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from random import randint

pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


def writeCsv(path, name, data, mode='w+'):
    '''list to csv'''
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(f'{path}/{name}', mode=f'{mode}', encoding='utf-8-sig', newline='') as f:
        for a in data:
            writer(f).writerow(a)
    print(f'{name} saved!')


def getData(driver, indexa, indexb, cata, catb):
    for i in range(5, 0, -1):
        print(f'{i} sec left to get data')
        sleep(1)
    pages = len(driver.find_elements(By.CSS_SELECTOR, '#gvDetail_ddlPageJump option'))
    if pages == 0:
        pages = 1
    print('total pages:', pages)
    for p in range(1, pages + 1):
        trs = driver.find_elements(By.CSS_SELECTOR, '#gvDetail tr')
        if pages == 1:
            rows = len(trs)
        else:
            rows = len(trs) - 1
        for i in range(1, rows):
            tds = trs[i].find_elements(By.CSS_SELECTOR, 'td')
            writeCsv(f'{pwd}/csv', 'fda.csv', [[
                indexa,
                indexb,
                cata,
                catb,
                tds[1].find_element(By.CSS_SELECTOR, 'a').text,
                tds[2].find_element(By.CSS_SELECTOR, 'span').text,
                tds[3].text,
                tds[4].text,
                tds[5].text,
                tds[6].text,
                tds[1].find_element(By.CSS_SELECTOR, 'a[href]').get_attribute('href')
            ]], mode='a+')
        if p < pages:
            driver.find_element(By.ID, 'gvDetail_btnNext').click()
            print(f'page {p}/{pages}')
            for i in range(randint(5, 10), 0, -1):
                print(f'{i} sec left to next page')
                sleep(1)
        else:
            for i in range(1, pages + 1):
                driver.back()
                sleep(1)


def startFilter(driver, a, b):
    print('filter start')
    caka = Select(driver.find_element(By.ID, 'ddlCaka'))
    cakb = Select(driver.find_element(By.ID, 'ddlCakb'))
    kind = Select(driver.find_element(By.ID, 'ddlBigKind'))
    mark = Select(driver.find_element(By.ID, 'ddlCanMark'))
    mark.select_by_index(0)
    mark.select_by_index(1)
    kind.select_by_index(0)
    kind.select_by_index(2)
    caka.select_by_index(0)
    caka.select_by_index(a)
    cakb.select_by_index(0)
    cakb.select_by_index(b)
    cata = caka.first_selected_option.text
    catb = cakb.first_selected_option.text
    print(f'filter finish')
    return [cata, catb]


def main():
    writeCsv(f'{pwd}/csv', 'fda.csv', [])
    url = 'https://info.fda.gov.tw/MLMS/H0001.aspx'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    for i in range(5, 0, -1):
        print(f'{i} sec left to start ca loop')
        sleep(1)
    cakalen = len(driver.find_elements(By.CSS_SELECTOR, '#ddlCaka option'))
    captcha = input('input captcha:')
    for a in range(1, cakalen + 1):
        caka = Select(driver.find_element(By.ID, 'ddlCaka'))
        caka.select_by_index(0)
        caka.select_by_index(a)
        cakblen = len(driver.find_elements(By.CSS_SELECTOR, '#ddlCakb option'))
        for b in range(9, cakblen + 1):
            print(f'a:{a} b:{b}')
            cat = startFilter(driver, a, b)
            print('send captcha')
            driver.find_element(By.ID, 'txtCheckCode').clear()
            driver.find_element(By.ID, 'txtCheckCode').send_keys(captcha)
            driver.find_element(By.ID, 'btnSearch').click()
            print('downloading')
            getData(driver, a, b, cat[0], cat[1])


main()
