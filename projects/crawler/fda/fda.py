import cv2
import os
import pytesseract
import numpy as np
from myfuc import b64Decode, writeCsv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from random import randint

pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


def pic_text(image):
    pytesseract.pytesseract.tesseract_cmd = r'D:/tools/Tesseract-OCR/tesseract.exe'
    return pytesseract.image_to_string(image)


def captchaText(img):
    height, width = img.shape[0], img.shape[1]
    width_new, height_new = 720, 160
    if width / height >= width_new / height_new:
        img = cv2.resize(img, (width_new, int(height * width_new / width)))
    else:
        img = cv2.resize(img, (int(width * height_new / height), height_new))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img = cv2.threshold(gray, 132, 255, cv2.THRESH_BINARY_INV)
    kernal = np.ones((4, 4), np.uint8)
    img = cv2.dilate(cv2.erode(img, kernal), kernal)
    for i in range(0, 10):
        img = cv2.dilate(cv2.erode(img, kernal), kernal)
    img = cv2.dilate(img, kernal, iterations=1)
    img = cv2.erode(img, np.ones((7, 7), np.uint8), iterations=1)
    img = cv2.dilate(img, np.ones((5, 5), np.uint8), iterations=1)
    cv2.imwrite(f'{pwd}/.temp/captcha2.png', img)
    return pic_text(img)


def getCaptcha(driver):
    driver.switch_to.frame('ValidationCodeImg')
    img_b64 = driver.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);
    """, driver.find_element(By.CSS_SELECTOR, 'body > img'))
    b64Decode(f'{pwd}/.temp', 'captcha.png', img_b64)
    driver.switch_to.default_content()
    captcha = captchaText(cv2.imread(f'{pwd}/.temp/captcha.png')).lower()
    excludeChar = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/§¥;“”'
    captcha = ''.join([x for x in captcha if x not in excludeChar])
    return captcha


def getData(driver, indexa, indexb, cata, catb):
    pages = len(driver.find_elements(By.CSS_SELECTOR, '#gvDetail_ddlPageJump option'))
    if pages == 0:
        pages = 1
    for p in range(1, pages + 1):
        trs = driver.find_elements(By.CSS_SELECTOR, '#gvDetail tr')
        for i in range(1, len(trs) - 1):
            tds = trs[i].find_elements(By.CSS_SELECTOR, 'td')
            writeCsv(f'{pwd}/csv', 'fda.csv', [[
                indexa,
                indexb,
                cata,
                catb,
                tds[1].find_element(By.CSS_SELECTOR, 'a').text,
                tds[2].find_element(By.CSS_SELECTOR, 'span').text,
                tds[3].text,
                tds[4].text,
                tds[5].text,
                tds[6].text,
                tds[1].find_element(By.CSS_SELECTOR, 'a[href]').get_attribute('href')
            ]], mode='a+')
        if p < pages:
            driver.find_element(By.ID, 'gvDetail_btnNext').click()
            print('next page')
            for i in range(randint(5, 10), 0, -1):
                print(f'{i} sec left')
                sleep(1)
        else:
            driver.find_element(By.ID, 'btnReSearch').click()
            for i in range(randint(5, 10), 0, -1):
                print(f'{i} sec left')
                sleep(1)


def main():
    writeCsv(f'{pwd}/csv', 'fda.csv', [])
    url = 'https://info.fda.gov.tw/MLMS/H0001.aspx'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    for i in range(randint(5, 10), 0, -1):
        print(f'{i} s left')
        sleep(1)
    kind = Select(driver.find_element(By.ID, 'ddlBigKind'))
    mark = Select(driver.find_element(By.ID, 'ddlCanMark'))
    cakb = Select(driver.find_element(By.ID, 'ddlCakb'))
    sleep(1)
    cakalen = len(driver.find_elements(By.CSS_SELECTOR, '#ddlCaka option'))
    for a in range(1, cakalen + 1):
        sleep(1)
        caka = Select(driver.find_element(By.ID, 'ddlCaka'))
        caka.select_by_index(0)
        caka.select_by_index(a)
        cakblen = len(driver.find_elements(By.CSS_SELECTOR, '#ddlCakb option'))
        for b in range(1, cakblen + 1):
            while True:
                try:
                    kind = Select(driver.find_element(By.ID, 'ddlBigKind'))
                    mark = Select(driver.find_element(By.ID, 'ddlCanMark'))
                    caka = Select(driver.find_element(By.ID, 'ddlCaka'))
                    cakb = Select(driver.find_element(By.ID, 'ddlCakb'))
                    mark.select_by_index(0)
                    mark.select_by_index(1)
                    kind.select_by_index(0)
                    kind.select_by_index(2)
                    caka.select_by_index(0)
                    caka.select_by_index(a)
                    cakb.select_by_index(0)
                    cakb.select_by_index(b)
                    cata = caka.first_selected_option.text
                    catb = cakb.first_selected_option.text
                    captcha = getCaptcha(driver)
                    print('captcha:', captcha)
                    if captcha == '':
                        for i in range(randint(5, 10), 0, -1):
                            print(f'{i} s left')
                            sleep(1)
                        driver.get(url)
                        continue
                    driver.find_element(By.ID, 'txtCheckCode').clear()
                    sleep(2)
                    driver.find_element(By.ID, 'txtCheckCode').send_keys(captcha)
                    getData(driver, a, b, cata, catb)
                except Exception as err:
                    print('retry')
                    driver.get(url)
                    for i in range(randint(5, 10), 0, -1):
                        print(f'{i} s left')
                        sleep(1)
                    continue
                break


main()
