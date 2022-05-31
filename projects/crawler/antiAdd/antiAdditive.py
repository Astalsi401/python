import os
import sys
sys.path.append('D:/Documents/python/myFunction')
from myfuc import writeCsv, readCsv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


chromedriver = 'D:/Tools/chromedriver'
os.chmod(chromedriver, 0o755)
driver = webdriver.Chrome(f'{chromedriver}/chromedriver')
pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


def getLinks():
    url = 'https://www.anti-a.org/tw/food'
    driver.get(url)
    for s in range(0, 40, 5):
        sleep(5)
        print(f'{40 - s} s')
    items = driver.find_element(By.CSS_SELECTOR, '.loadMoreButton').get_attribute('data-items-left')
    pages = round(float(items) / 20)
    for a in range(0, pages):
        driver.find_element(By.CSS_SELECTOR, '.loadMoreButton').click()
        print(f'page {a}, total {pages}')
        sleep(2)
    res = driver.find_elements(By.CSS_SELECTOR, '.sqs-gallery .summary-item')
    data = []
    for a in res:
        row = [
            a.find_element(By.CSS_SELECTOR, '.summary-metadata-item--cats').text,
            a.find_element(By.CSS_SELECTOR, '.summary-title').text,
            a.find_element(By.CSS_SELECTOR, 'a[href]').get_attribute('href')
        ]
        data.append(row)
    writeCsv(f'{pwd}/csv', 'links.csv', data)


def getData(url, driver):
    driver.get(url[1])
    for s in range(0, 30, 5):
        sleep(5)
        print(f'{30 - s} s left')
    res = driver.find_elements(By.CSS_SELECTOR, '.sqs-block.html-block.sqs-block-html')[1].find_elements(By.CSS_SELECTOR, 'p')
    text = ''
    for b in res:
        text += f'{b.text}\r\n'
    data = [[url[0], url[1], text]]
    writeCsv(f'{pwd}/csv', 'certificateInfo.csv', data, mode='a+')


def getDatas():
    urls = readCsv(f'{pwd}/csv', 'links.csv')
    urlsLength = len(urls)
    writeCsv(f'{pwd}/csv', 'certificateInfo.csv', [])
    for a in urls:
        getData(a, driver)
        urlsLength -= 1
        print(f'{urlsLength} left, about {(urlsLength)*30/60/60} hr')


def main():
    getLinks()
    getDatas()
    driver.close()


if __name__ == '__main__':
    main()
