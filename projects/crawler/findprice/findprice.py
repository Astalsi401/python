import os
import pandas as pd
from csv import writer, reader
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook, load_workbook

pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
chop = Options()
chop.add_extension('D:/Tools/driver/4.46.2_0.crx')  # adblock
chop.add_extension('D:/Tools/driver/windscribe_3.4.3_0.crx')


def alpha(alpha):
    '''
    26進位英數互換
    '''
    if type(alpha) == str:
        alpha = alpha.upper()
        assert(isinstance(alpha, str))
        return sum([(ord(n) - 64) * 26**i for i, n in enumerate(list(alpha)[::-1])])
    elif type(alpha) == int:
        assert(isinstance(alpha, int) and alpha > 0)
        num = [chr(i) for i in range(65, 91)]
        ret = []
        while alpha > 0:
            alpha, m = divmod(alpha - 1, len(num))
            ret.append(num[m])
        return ''.join(ret[::-1])


def xlsx(f, sheet, data, start):
    '''
    引入openpyxl後再使用
    list to excel
    f = openpyxl.load_workbook(path)
    sheet = sheet name
    data = 資料(list)
    start = excel開始的位置，如['A', '1']
    '''
    try:
        ws = f[sheet]
    except KeyError:
        f.create_sheet(sheet, 0)
        ws = f[sheet]
    start = start[0] + start[1]
    end = alpha(alpha(start[0]) + len(data[0]) - 1) + str(int(start[1]) + len(data) - 1)
    for i, r in enumerate(ws[start:end]):
        for j, c in enumerate(r):
            c.value = data[i][j]


def writeCsv(path, name, data, mode='w+', enc='utf-8-sig'):
    '''list to csv'''
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(f'{path}/{name}', mode=mode, encoding=enc, newline='') as f:
        for a in data:
            writer(f).writerow(a)
    print(f'{name} saved!')


def readCsv(path, name, enc='utf-8-sig'):
    '''csv to list'''
    with open(f'{path}/{name}', mode='r', encoding=enc, newline='') as f:
        return [a for a in reader(f)]


def spread(arg):
    res = []
    for i in arg:
        if isinstance(i, list):
            res.extend(i)
        else:
            res.append(i)
    return res


def vpn(driver, mode):
    print(f'vpn {mode}', end='')
    driver.switch_to.window(driver.window_handles[0])
    for i in range(0, 5):
        sleep(1)
        print('.', end='')
    btn = driver.find_element(By.XPATH, '//*[@id="app-frame"]/div/div[4]/div[1]/div/div[1]/div/div[3]/button')
    if mode == 'on':
        if btn.get_attribute('class') == 'css-1ek69w9-SimpleButton-baseStyle-SimpleButtonStyle-ButtonContainer euzhj6i0':
            btn.click()
    elif mode == 'off':
        if btn.get_attribute('class') == 'css-37am5c-SimpleButton-baseStyle-SimpleButtonStyle-ButtonContainer euzhj6i0':
            btn.click()
    driver.switch_to.window(driver.window_handles[1])


def vpnLogin(driver):
    driver.switch_to.window(driver.window_handles[0])
    vpn = 'chrome-extension://hnmpcagpplmpfojmgmnngilcnanddlhb/popup.html'
    driver.get(vpn)
    username = 'astalsi401'
    password = 'CnAmCpg9lIWN'
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
    driver.switch_to.window(driver.window_handles[1])


def checkExists(web, path, mode='text', selector='css'):
    try:
        if path == '':
            return ''
        elif mode == 'text':
            if selector == 'xpath':
                print(f'selector: {selector}')
                print(f'text: {web.find_element(By.XPATH, path).text}')
                return web.find_element(By.XPATH, path).text
            else:
                return web.find_element(By.CSS_SELECTOR, path).text
        elif mode == 'href':
            return web.find_element(By.CSS_SELECTOR, path).get_attribute('href')
    except NoSuchElementException:
        return ''


def getData(product, j, i, row, page=1, selector='css'):
    res = {
        'source': row['source'],
        'key': row['key'],
        'site': checkExists(product, row['site']),
        'price': checkExists(product, row['price'], selector=selector),
        'name': checkExists(product, row['name'], selector=selector),
        'event': spread([checkExists(product, e) for e in row['event']]),
        'link': checkExists(product, row['link'], 'href')
    }
    df = pd.DataFrame.from_dict([res])
    source = row['source']
    if i == 0 and j == 0 and page == 1:
        df.to_csv(f'{pwd}/csv/{source}.csv', index=False, header=True, mode='w+')
    else:
        df.to_csv(f'{pwd}/csv/{source}.csv', index=False, header=False, mode='a+')


def google(driver):
    for i, key in enumerate(readCsv(f'{pwd}/csv', 'keywords.csv')):
        url = f'https://www.google.com/search?q={key[0]}&tbm=shop'
        driver.get(url)
        row = {
            'source': 'google',
            'key': key[0],
            'site': '.aULzUe.IuHnof',
            'price': '.a8Pemb.OFFNJ',
            'name': '.Xjkr3b',
            'event': ['.vEjMR'],
            'link': 'a.shntl[href]',
        }
        print(f'keywords: {i}/{len(key)}, {row["source"]}')
        for j, product in enumerate(driver.find_elements(By.CSS_SELECTOR, '.sh-pr__product-results-grid.sh-pr__product-results .sh-dgr__content')):
            getData(product, j, i, row)


def findprice(driver):
    for i, key in enumerate(readCsv(f'{pwd}/csv', 'keywords.csv')):
        url = f'https://www.findprice.com.tw/g/{key[0]}'
        driver.get(url)
        sleep(5)
        row = {
            'source': 'findprice',
            'key': key[0],
            'site': '.GoodsMname',
            'price': '.rec-price-20',
            'name': '.GoodsGname',
            'event': ['.act_div', '.discount_div'],
            'link': '.GoodsGname a.ga[href]',
        }
        page = 1
        while driver.find_elements(By.CSS_SELECTOR, '#pg-next'):
            print(f'keywords: {i}/{len(key)}, page: {page}, {row["source"]}')
            for j, product in enumerate(driver.find_elements(By.CSS_SELECTOR, '#g_div .divGoods')):
                getData(product, j, i, row, page)
            driver.find_element(By.CSS_SELECTOR, '#pg-next').click()
            page += 1
            sleep(5)
        print(f'keywords: {i}/{len(key)}, page: {page}, {row["source"]}')
        for j, product in enumerate(driver.find_elements(By.CSS_SELECTOR, '#g_div .divGoods')):
            getData(product, j, i, row, page)


def momoLogin(driver):
    driver.find_element(By.CSS_SELECTOR, '#LOGINSTATUS').click()
    sleep(5)
    driver.find_element(By.CSS_SELECTOR, '#loginForm #memId').send_keys('0906669085')
    driver.find_element(By.CSS_SELECTOR, '#loginForm #passwd_show').click()
    driver.find_element(By.CSS_SELECTOR, '#loginForm #passwd').send_keys('Ak2jLteBfL6ehyy')
    sleep(2)
    driver.find_element(By.CSS_SELECTOR, '.loginBtn input').click()
    sleep(5)


def momoCoupon(driver):
    vpn(driver, 'off')
    writeCsv(f'{pwd}/csv', 'momo折價券.csv', [['source', 'key', 'price', 'name', '折價券名稱', '折價券面額', '折價後金額', 'link']], mode='w+')
    urls = []
    for url in readCsv(f'{pwd}/csv', 'momo.csv'):
        if '折價券' in url[5]:
            urls.append(url)
    for url in urls:
        driver.get(url[6])
        sleep(5)
        momoLogin(driver)
        driver.find_element(By.CSS_SELECTOR, '.showCoupon').click()
        sleep(2)
        for trs in driver.find_elements(By.CSS_SELECTOR, '.couponList tbody tr'):
            tds = trs.find_elements(By.CSS_SELECTOR, 'td')
            row = [url[0], url[1], url[3], url[4], tds[0].text, tds[1].text, tds[2].text, url[6]]
            writeCsv(f'{pwd}/csv', 'momo折價券.csv', [row], mode='a+')
        print(f'momo coupon saved')
    vpn(driver, 'on')


def momo(driver):
    for i, key in enumerate(readCsv(f'{pwd}/csv', 'keywords.csv')):
        driver.get(f'https://www.momoshop.com.tw/search/searchShop.jsp?keyword={key[0]}')
        sleep(5)
        remind = driver.find_element(By.CSS_SELECTOR, '.remindBox').text
        row = ['momo', key[0], remind, '', '', '', '']
        if remind != '':
            if i == 0:
                writeCsv(f'{pwd}/csv', 'momo.csv', [row], mode='w+')
            else:
                writeCsv(f'{pwd}/csv', 'momo.csv', [row], mode='a+')
            break
        row = {
            'source': 'momo',
            'key': key[0],
            'site': '',
            'price': '.price',
            'name': '.prdName',
            'event': ['.iconArea'],
            'link': 'a.goodsUrl[href]',
        }
        page = 1
        while driver.find_elements(By.XPATH, "//*[contains(text(), '下一頁')]"):
            print(f'keywords: {i}/{len(key)}, page: {page}')
            for j, product in enumerate(driver.find_elements(By.CSS_SELECTOR, '.listArea li')):
                getData(product, j, i, row, page)
            driver.find_elements(By.XPATH, "//*[contains(text(), '下一頁')]")[0].click()
            page += 1
            sleep(5)
        print(f'keywords: {i}/{len(key)}, page: {page}, {row["source"]}')
        for j, product in enumerate(driver.find_elements(By.CSS_SELECTOR, '.listArea li')):
            getData(product, j, i, row, page)


def watsons(driver):
    for i, key in enumerate(readCsv(f'{pwd}/csv', 'keywords.csv')):
        url = f'https://www.watsons.com.tw/search?text={key[0]}&pageSize=64'
        driver.set_window_size(1080, 1000)
        driver.get(url)
        sleep(5)
        remind = driver.find_element(By.CSS_SELECTOR, '.SearchResultText.has-components.ng-star-inserted').text
        row = ['watsons', key[0], remind, '', '', '', '']
        if '找不到相符結果' in remind:
            if i == 0:
                writeCsv(f'{pwd}/csv', 'watsons.csv', [row], mode='w+')
            else:
                writeCsv(f'{pwd}/csv', 'watsons.csv', [row], mode='a+')
            break
        row = {
            'source': 'watsons',
            'key': key[0],
            'site': '',
            'price': '.productPrice',
            'name': '.productName',
            'event': ['.productHighlight'],
            'link': '.productName a[href]',
        }
        page = 1
        print(f'keywords: {i}/{len(key)}, page: {page}, {row["source"]}')
        for j, product in enumerate(driver.find_elements(By.CSS_SELECTOR, 'e2-product-list e2-product-tile')):
            getData(product, j, i, row, page)


def cosmed(driver):
    for i, key in enumerate(readCsv(f'{pwd}/csv', 'keywords.csv')):
        url = f'https://shop.cosmed.com.tw/v2/Search?shopId=2131&q={key[0]}'
        driver.get(url)
        row = {
            'source': 'cosmed',
            'key': key[0],
            'site': '',
            'price': '//div/div/a/div/div[2]/div[2]/div[1]/div[2]',
            'name': '//div/div/a/div/div[2]/div[1]',
            'event': [''],
            'link': 'a[href]',
        }
        print(f'keywords: {i}/{len(key)}, {row["source"]}')
        for j, product in enumerate(driver.find_elements(By.CSS_SELECTOR, '.column-grid-container__column')):
            getData(product, j, i, row, selector='xpath')


def exportXlsx():
    try:
        f = load_workbook(filename=f'{pwd}/findprice.xlsx')
    except FileNotFoundError:
        f = Workbook()
    for file in ['cosmed.csv', 'findprice.csv', 'google.csv', 'momo.csv', 'momo折價券.csv', 'watsons.csv']:
        data = readCsv(f'{pwd}/csv', file)
        sheet = file.replace('.csv', '')
        xlsx(f, sheet, data, ['A', '1'])
    f.save(f'{pwd}/findprice.xlsx')


def main():
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chop)
    # vpnLogin(driver)
    # vpn(driver, 'off')
    # vpn(driver, 'on')
    # google(driver)
    # findprice(driver)
    # watsons(driver)
    # cosmed(driver)
    # momo(driver)
    # momoCoupon(driver)
    exportXlsx()


if __name__ == '__main__':
    main()
