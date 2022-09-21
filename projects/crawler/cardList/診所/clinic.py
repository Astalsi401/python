import re
from os.path import dirname, abspath
from myfuc import readCsv, writeCsv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))


def getLinks(type_clinic):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.nhi.gov.tw/QueryN_New/QueryN/Query3')
    w = WebDriverWait(driver, 10)
    submit = w.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]')))
    citySelect = Select(driver.find_element(By.CSS_SELECTOR, '#CountyAreaCode'))
    for city in ['臺北市', '新北市', '基隆市', '新竹市', '桃園市', '新竹縣', '宜蘭縣']:
        citySelect.select_by_visible_text(city)
        spTypeSelect = Select(driver.find_element(By.CSS_SELECTOR, '#Special_Type'))
        spTypeSelect.select_by_visible_text(type_clinic)
        # hospTypeSelect = Select(driver.find_element(By.CSS_SELECTOR, '#HospType'))
        # hospTypeSelect.select_by_visible_text(type_clinic)
        submit.click()
        w.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#btnPrint'))).click()
        try:
            table = w.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#GridTable tbody tr')))
            for row in table:
                tds = row.find_elements(By.CSS_SELECTOR, 'td')
                res = [tds[0].text, tds[1].text, '', '', tds[2].text, '', type_clinic]
                writeCsv(pwd, f'orgInfo.csv', [res], 'a+')
        except TimeoutException:
            pass
        driver.get('https://www.nhi.gov.tw/QueryN_New/QueryN/Query3')
        submit = w.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]')))
        citySelect = Select(driver.find_element(By.CSS_SELECTOR, '#CountyAreaCode'))


if __name__ == '__main__':
    getLinks()
