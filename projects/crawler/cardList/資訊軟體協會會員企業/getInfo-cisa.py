import re
from os.path import dirname, abspath
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from myfuc import List, readCsv
from requests import get
from bs4 import BeautifulSoup as bs

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


def getLinks(driver):
    res = [[a.get_attribute('title'), a.get_attribute('href')] for a in driver.find_elements(By.CSS_SELECTOR, '#Eservice .card a')]
    List(res).writeCsv(pwd, 'orgLinks.csv', mode='a+')


def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.cisanet.org.tw/eBook/Index')
    cat1 = Select(driver.find_element(By.CSS_SELECTOR, '#class1'))
    cat1.select_by_value('D')
    sleep(1)
    cat2 = Select(driver.find_element(By.CSS_SELECTOR, '#class2'))
    cat2.select_by_value('DJ')
    driver.find_element(By.CSS_SELECTOR, '#buttonSearch2').click()
    for i in range(0, 3):
        sleep(2)
        getLinks(driver)
        try:
            driver.find_element(By.CSS_SELECTOR, '#Eservice a.page-link[title="next page"]').click()
        except:
            pass


def pagedl(link):
    res = get(link[1], headers=header)
    sleep(1)
    open(f'{pwd}/html/{link[0]}.html', encoding='utf-8', mode='w+').write(res.text)


def main2():
    for link in readCsv(pwd, 'orgLinks.csv'):
        pagedl(link)


def getInfo(link):
    soup = bs(open(f'{pwd}/html/{link[0]}.html', encoding='utf-8'), 'html.parser')
    res = {
        'site': '',
        'tel': ''
    }
    for li in soup.select('.col-md-12 ul li'):
        if '聯絡電話：' in li.text:
            res['tel'] = li.text.replace('聯絡電話：', '').replace(' ', '').replace('\n', '')
    List([[
        link[0],
        '',
        '',
        '',
        res['tel'],
        '',
        '資訊軟體協會會員企業',
        '',
    ]]).writeCsv(pwd, 'orgInfo.csv', mode='a+')


def main3():
    List(colname).writeCsv(pwd, 'orgInfo.csv', mode='w+')
    for link in readCsv(pwd, 'orgLinks.csv'):
        getInfo(link)


if __name__ == '__main__':
    main3()
