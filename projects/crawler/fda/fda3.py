import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from myfuc import writeCsv
from random import randint

pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


def getData(driver):
    pages = len(driver.find_elements(By.CSS_SELECTOR, '#gvDetail_ddlPageJump option'))
    for p in range(1, pages + 1):
        print(f'page {p}/{pages}')
        trs = driver.find_elements(By.CSS_SELECTOR, '#gvDetail tr')
        for i in range(1, len(trs) - 1):
            writeCsv(f'{pwd}/csv', 'fda3.csv', [[td.text for td in trs[i].find_elements(By.CSS_SELECTOR, 'td')]], mode='a+')
        if p < pages:
            driver.find_element(By.ID, 'gvDetail_btnNext').click()
        for i in range(randint(10, 20), 1, -1):
            print(i)
            sleep(1)


def main():
    writeCsv(f'{pwd}/csv', 'fda3.csv', [])
    url = 'https://info.fda.gov.tw/MLMS/H0005.aspx'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    area = Select(driver.find_element(By.ID, 'ddlMedifact'))
    area.select_by_index(1)
    driver.find_element(By.ID, 'btnSearch').click()
    getData(driver)


if __name__ == '__main__':
    main()
