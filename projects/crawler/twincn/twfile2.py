from cgi import print_form
import os
from csv import writer, reader
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
from pandas import unique

pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
chop = webdriver.ChromeOptions()
chop.add_extension('D:/Tools/driver/4.46.2_0.crx')  # adblock
chop.add_extension('D:/Tools/driver/windscribe_3.4.3_0.crx')


def readCsv(path, name):
    '''csv to list'''
    with open(f'{path}/{name}', mode='r', encoding='utf-8-sig', newline='') as f:
        return [a for a in reader(f)]


def writeCsv(path, name, data, mode='w+'):
    '''list to csv'''
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(f'{path}/{name}', mode=f'{mode}', encoding='utf-8-sig', newline='') as f:
        for a in data:
            writer(f).writerow(a)
    print(f'{name} saved!')


def getKeys():
    keys = [row[2] for row in readCsv(f'{pwd}/csv', 'fda3.csv')]
    writeCsv(f'{pwd}/csv', 'keys.csv', [])
    for key in unique(keys).tolist():
        writeCsv(f'{pwd}/csv', 'keys.csv', [[key]], mode='a+')


def reconnect(driver):
    print('vpn reconnect')
    driver.switch_to.window(driver.window_handles[0])
    sleep(5)
    print('vpn off', end='')
    driver.find_element(By.XPATH, '//*[@id="app-frame"]/div/div[4]/div[1]/div/div[1]/div/div[3]/button').click()
    for i in range(0, 5):
        sleep(1)
        print('.', end='')
    print('vpn on')
    driver.find_element(By.XPATH, '//*[@id="app-frame"]/div/div[4]/div[1]/div/div[1]/div/div[3]/button').click()
    sleep(5)
    driver.switch_to.window(driver.window_handles[1])


def vpn(driver):
    driver.switch_to.window(driver.window_handles[0])
    vpn = 'chrome-extension://hnmpcagpplmpfojmgmnngilcnanddlhb/popup.html'
    driver.get(vpn)
    username = 'link9186'
    password = 'l3puod26'
    w = WebDriverWait(driver, 10)
    w.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-frame"]/div/button[2]')))
    driver.find_element(By.XPATH, '//*[@id="app-frame"]/div/button[2]').click()
    print('login windscribe')
    w.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-frame"]/div/div/form/div[1]/div[2]/input')))
    driver.find_element(By.XPATH, '//*[@id="app-frame"]/div/div/form/div[1]/div[2]/input').send_keys(username)
    w.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-frame"]/div/div/form/div[2]/div[2]/input')))
    driver.find_element(By.XPATH, '//*[@id="app-frame"]/div/div/form/div[2]/div[2]/input').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="app-frame"]/div/div/form/div[3]/button').click()

    w.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-frame"]/div/button[2]')))
    driver.find_element(By.XPATH, '//*[@id="app-frame"]/div/button[2]').click()
    reconnect(driver)
    driver.switch_to.window(driver.window_handles[1])


def getLinks():
    keys = readCsv(f'{pwd}/csv', 'keys.csv')
    url = 'https://www.twfile.com/'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chop)
    vpn(driver)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
    for j in range(4188, len(keys)):
        print(f'key: {j}')
        while True:
            try:
                driver.get(url)
                for i in range(randint(20, 30), 0, -1):
                    if i != 1:
                        print(i, end=' ')
                    else:
                        print(i)
                    sleep(1)
                driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_stxt').send_keys(keys[j][0])
                driver.find_element(By.ID, 'button-addon2').click()
                sleep(2)
                for tr in driver.find_elements(By.CSS_SELECTOR, '.container .table.table-striped tbody tr'):
                    link = tr.find_elements(By.CSS_SELECTOR, 'td')[1].find_element(By.CSS_SELECTOR, 'a[href]').get_attribute('href')
                    result = tr.find_elements(By.CSS_SELECTOR, 'td')[1].text
                    if keys[j][0] in result:
                        row = [keys[j][0], result, link]
                        writeCsv(f'{pwd}/csv', 'twfile.csv', [row], mode='a+')
            except:
                reconnect(driver)
                continue
            break


def main():
    getLinks()


if __name__ == '__main__':
    main()
