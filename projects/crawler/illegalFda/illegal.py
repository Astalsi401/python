import os
import logging
from csv import writer, reader
from datetime import date
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


def writeCsv(path, name, data, mode='w+'):
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(f'{path}/{name}', mode=f'{mode}', encoding='utf-8-sig', newline='') as f:
        for a in data:
            writer(f).writerow(a)
    logging.info(f'{name} saved!')


def readCsv(path, name):
    return [c for c in reader(open(f'{path}/{name}', mode='r', encoding='utf-8-sig', newline=''))]


def yearsCalc(yearsAgo=0):
    '''列出最近3年年份'''
    a = []
    for b in range(0, yearsAgo):
        a.append(str(date.today().year - b))
    return a


def getLists(keyword, driver, data):
    sleepTime = randint(10, 20)
    res = driver.find_elements(By.CSS_SELECTOR, '.table_list tr')
    if len(res) == 0:
        writeCsv(f'{pwd}/csv', '違規紀錄.csv', [[keyword[0], '無違規紀錄']], mode='a+')
        for a in range(0, sleepTime):
            logging.info(f'wait {sleepTime - a} sec')
            sleep(1)
        return [keyword[0], len(res)]
    lastYear = res[len(res) - 1].find_elements(By.CSS_SELECTOR, 'td')[3].find_elements(By.CSS_SELECTOR, 'li')[1].text.split('.')[0]
    del res[0]
    for a in res:
        b = a.find_elements(By.CSS_SELECTOR, 'td')
        date = b[3].find_elements(By.CSS_SELECTOR, 'li')[1].text
        yearRange = yearsCalc(3)
        if str(1911 + int(date[0:3])) in yearRange:
            product = b[1].text
            url = b[1].find_element(By.CSS_SELECTOR, 'a[href]').get_attribute('href')
            company = b[2].text
            data.append([company, date, product, url])
            logging.info([company, date, product, url])
        elif str(1911 + int(date[0:3])) < yearRange[len(yearRange) - 1]:
            writeCsv(f'{pwd}/csv', '違規紀錄.csv', [[keyword[0], '違規紀錄三年以前']], mode='a+')
    for a in range(0, sleepTime):
        logging.info(f'wait {sleepTime - a} sec')
        sleep(1)
    return [lastYear, len(res)]


def getLinks(driver, keyword, data):
    driver.find_element(By.CSS_SELECTOR, '#ctl00_Content_txtVioCompany').clear()
    driver.find_element(By.CSS_SELECTOR, '#ctl00_Content_txtVioCompany').send_keys(keyword[0])
    driver.find_element(By.CSS_SELECTOR, '#ctl00_Content_btnSubmit').click()
    while True:
        lastYear = getLists(keyword, driver, data)
        if lastYear[1] == 0:
            logging.info(f'no result')
            break
        elif str(int(lastYear[0]) + 1911) in yearsCalc(3) and int(lastYear[0]) == 11:
            logging.info('next page')
            driver.find_element(By.CSS_SELECTOR, 'a.next').click()
        else:
            break
    writeCsv(f'{pwd}/csv', '違規紀錄_連結.csv', data)


def getVio(driver):
    links = readCsv(f'{pwd}/csv', '違規紀錄_連結.csv')
    data = []
    for link in links:
        driver.get(link[3])
        sleepTime = randint(10, 20)
        for a in range(0, sleepTime):
            logging.info(f'wait {sleepTime - a} sec')
            sleep(1)
        row = link[:-1]
        for a in driver.find_elements(By.CSS_SELECTOR, '.table_data tr'):
            b = a.find_element(By.CSS_SELECTOR, 'th').text
            if '違規情節' in b:
                row.append(a.find_element(By.CSS_SELECTOR, 'td').text)
            elif '查處情形' in b:
                row.append(a.find_element(By.CSS_SELECTOR, 'td').text)
        row.append(link[-1])
        data.append(row)
    writeCsv(f'{pwd}/csv', '違規紀錄.csv', data, mode='a+')
    if os.path.exists(f'{pwd}/csv/違規紀錄_連結.csv'):
        os.remove(f'{pwd}/csv/違規紀錄_連結.csv')


def main():
    data = []
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = 'https://pmds.fda.gov.tw/illegalad/CaseSearch.aspx'
    writeCsv(f'{pwd}/csv', '違規紀錄.csv', [])
    driver.get(url)
    for keyword in readCsv(f'{pwd}/csv', 'keywords.csv'):
        try:
            getLinks(driver, keyword, data)
        except Exception as e:
            writeCsv(f'{pwd}/csv', '違規紀錄.csv', [[keyword, '抓取失敗!']], mode='a+')
            logging.warning(keyword[0], e, 'fail!')
    getVio(driver)
    driver.close()


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, filename=f'{pwd}/.tmp/viorec.log')
    main()
