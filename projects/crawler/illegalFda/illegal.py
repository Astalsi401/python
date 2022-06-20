import os
import sys
sys.path.append('D:/Documents/python/myFunction')
from random import randint
from myfuc import writeCsv, readCsv, yearsCalc
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

chromedriver = 'D:/Tools/chromedriver'
pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
os.chmod(chromedriver, 0o755)


def getLists(driver, data):
    res = driver.find_elements(By.CSS_SELECTOR, '.table_list tr')
    lastYear = res[len(res) - 1].find_elements(By.CSS_SELECTOR, 'td')[3].find_elements(By.CSS_SELECTOR, 'li')[1].text[0:3]
    del res[0]
    for a in res:
        b = a.find_elements(By.CSS_SELECTOR, 'td')
        date = b[3].find_elements(By.CSS_SELECTOR, 'li')[1].text
        if str(1911 + int(date[0:3])) in yearsCalc(3):
            product = b[1].text
            url = b[1].find_element(By.CSS_SELECTOR, 'a[href]').get_attribute('href')
            company = b[2].text
            data.append([company, date, product, url])
            print([company, date, product, url])
    sleepTime = randint(5, 10)
    print(f'sleep {sleepTime} sec')
    sleep(sleepTime)
    return lastYear


def getLinks(keyword, data):
    driver = webdriver.Chrome(f'{chromedriver}/chromedriver')
    # driver.minimize_window()
    url = 'https://pmds.fda.gov.tw/illegalad/CaseSearch.aspx'
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, '#ctl00_Content_txtVioCompany').send_keys(keyword)
    driver.find_element(By.CSS_SELECTOR, '#ctl00_Content_btnSubmit').click()
    while True:
        lastYear = getLists(driver, data)
        if str(int(lastYear) + 1911) in yearsCalc(3):
            print('next page')
            driver.find_element(By.CSS_SELECTOR, 'a.next').click()
        else:
            break
    writeCsv(f'{pwd}/csv', '違規紀錄_連結.csv', data)
    driver.close()
    driver.quit()


def getVio():
    links = readCsv(f'{pwd}/csv', '違規紀錄_連結.csv')
    driver = webdriver.Chrome(f'{chromedriver}/chromedriver')
    data = []
    for link in links:
        url = link[3]
        driver.get(url)
        sleepTime = randint(5, 10)
        print(f'sleep {sleepTime} sec')
        sleep(sleepTime)
        row = [link[0], link[1], link[2]]
        for a in driver.find_elements(By.CSS_SELECTOR, '.table_data tr'):
            b = a.find_element(By.CSS_SELECTOR, 'th').text
            if '違規情節' in b:
                row.append(a.find_element(By.CSS_SELECTOR, 'td').text)
            elif '查處情形' in b:
                row.append(a.find_element(By.CSS_SELECTOR, 'td').text)
        data.append(row)
    driver.close()
    driver.quit()
    writeCsv(f'{pwd}/csv', '過去違規紀錄.csv', data)


def main():
    data = []
    for keyword in readCsv(f'{pwd}/csv', 'keywords.csv'):
        getLinks(keyword, data)
    getVio()


if __name__ == '__main__':
    main()
