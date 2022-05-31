import os
from csv import DictWriter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from myfuc import writeCsv

pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


def getData(driver):
    trs = driver.find_elements(By.CSS_SELECTOR, '.staff tbody tr.show1')
    for i in range(1, len(trs)):
        tds = trs[i].find_elements(By.CSS_SELECTOR, 'td')
        row = {
            'companyName': tds[1].find_element(By.CSS_SELECTOR, '.txt1').text,
            'companyName_en': tds[1].find_element(By.CSS_SELECTOR, '.txt2').text,
            'mainProducts': tds[2].find_element(By.CSS_SELECTOR, '.txt1').text
        }
        for a in tds[3].find_elements(By.CSS_SELECTOR, 'div'):
            className = a.find_element(By.CSS_SELECTOR, 'i').get_attribute('class')
            if 'fa-map-marker-alt' in className:
                row['location'] = a.text
            elif 'fa-phone' in className:
                row['tel'] = a.text
            elif 'fa-fax' in className:
                row['fax'] = a.text
            elif 'fa-envelope-square' in className:
                row['mail'] = a.text
            elif 'fa-link' in className:
                row['site'] = a.text
            elif 'fa-industry' in className:
                row['factory'] = a.text
        with open(f'{pwd}/csv/garment.csv', 'a+') as f:
            writer = DictWriter(f, restval='', fieldnames=[
                'companyName',
                'companyName_en',
                'mainProducts',
                'location',
                'tel',
                'fax',
                'mail',
                'site',
                'factory',
            ])
            writer.writerow(row)


def garment():
    url = 'https://www.taiwan-garment.org.tw/mod/staff/index.php'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    for p in range(1, 17):
        print('sleep 10 sec')
        sleep(10)
        getData(driver)
        if p < 16:
            driver.find_element(By.CSS_SELECTOR, 'a.rarr').click()


def main():
    writeCsv(f'{pwd}/csv', 'garment.csv', [])
    garment()


main()
