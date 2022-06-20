import os
from re import T
import pandas as pd
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
chop = Options()
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
    print('connect vpn')
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
    sleep(5)
    driver.switch_to.window(driver.window_handles[1])


def getData():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chop)
    urls = readCsv(f'{pwd}/csv', 'twfile.csv')
    vpn(driver)
    for j in range(0, len(urls)):
        while True:
            try:
                print(f'index: {j}/{len(urls)}')
                driver.get(urls[j][2])
                for i in range(randint(20, 30), 0, -1):
                    if i != 1:
                        print(i, end=' ')
                    else:
                        print(i)
                    sleep(1)
                res = {}
                trs = driver.find_elements(By.CSS_SELECTOR, '#basic-data tr')
                for i in range(0, len(trs) - 2):
                    tds = trs[i].find_elements(By.CSS_SELECTOR, 'td')
                    name = tds[0].text.replace('\r', '').replace('\n', '')
                    res[f'{name}'] = tds[1].text
                df = pd.DataFrame.from_dict([res])
                if j == 0:
                    df.to_csv(f'{pwd}/csv/basicData.csv', index=False, header=True, mode='w+')
                else:
                    df.to_csv(f'{pwd}/csv/basicData.csv', index=False, header=False, mode='a+')
            except:
                reconnect(driver)
                continue
            break


def main():
    getData()


if __name__ == '__main__':
    main()
