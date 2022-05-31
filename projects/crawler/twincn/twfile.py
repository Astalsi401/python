from operator import mod
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from myfuc import writeCsv, readCsv
from random import randint
from pandas import unique

pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
chop = webdriver.ChromeOptions()
chop.add_extension('D:/Tools/driver/4.46.2_0.crx')


def getLinks():
    writeCsv(f'{pwd}/csv', 'twfile.csv', [])
    keys = [row[2] for row in readCsv(f'{pwd}/csv', 'fda3.csv')]
    url = 'https://www.twfile.com/'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=chop)
    for key in unique(keys).tolist():
        driver.get(url)
        sleep(10)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_stxt').send_keys(key)
        driver.find_element(By.ID, 'button-addon2').click()
        for tr in driver.find_elements(By.CSS_SELECTOR, '.container .table.table-striped tbody tr'):
            link = tr.find_elements(By.CSS_SELECTOR, 'td')[1].find_element(By.CSS_SELECTOR, 'a[href]').get_attribute('href')
            result = tr.find_elements(By.CSS_SELECTOR, 'td')[1].text
            if key == result:
                row = [key, result, link]
                print(row)
                writeCsv(f'{pwd}/csv', 'twfile.csv', [row], mode='a+')
            else:
                print(f'{key} no result')


def main():
    getLinks()


if __name__ == '__main__':
    main()
