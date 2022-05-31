import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
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
    driver.get(url)
    for key in unique(keys).tolist():
        sleep(2)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_stxt').send_keys(key)
        driver.find_element(By.ID, 'search-btn').click()
        sleep(2)
        for a in driver.find_elements(By.CSS_SELECTOR, '.table.table-striped tbody tr'):
            link = a.find_elements(By.CSS_SELECTOR, 'td')[1]
            print(link)
            # .find_element(By.CSS_SELECTOR, 'a[href]').get_attribute('href')
            writeCsv(f'{pwd}/csv', 'twincn.csv', [[key, link]])
        driver.get(url)


def main():
    getLinks()


if __name__ == '__main__':
    main()
