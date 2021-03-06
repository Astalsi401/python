from operator import mod
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from myfuc import writeCsv, readCsv
from random import randint
from pandas import unique

pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


def getLinks():
    writeCsv(f'{pwd}/csv', 'twincn.csv', [])
    keys = [row[2] for row in readCsv(f'{pwd}/csv', 'fda3.csv')]
    url = 'https://www.twincn.com/'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    w = WebDriverWait(driver, 10)
    for key in unique(keys).tolist():
        driver.get(url)
        w.until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_stxt')))
        driver.execute_script("window.stop();")
        sleep(10)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_stxt').send_keys(key)
        driver.find_element(By.ID, 'search-btn').click()
        w.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#services td')))
        driver.execute_script("window.stop();")
        for tr in driver.find_elements(By.CSS_SELECTOR, '#services .table.table-striped tbody tr'):
            link = tr.find_elements(By.CSS_SELECTOR, 'td')[1].find_element(By.CSS_SELECTOR, 'a[href]').get_attribute('href')
            result = tr.find_elements(By.CSS_SELECTOR, 'td')[1].text
            row = [key, result, link]
            print(row)
            writeCsv(f'{pwd}/csv', 'twincn.csv', [row], mode='a+')


def main():
    getLinks()


if __name__ == '__main__':
    main()
