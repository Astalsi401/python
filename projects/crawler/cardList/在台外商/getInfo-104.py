# -- coding:UTF-8 --
from tryRequest import pageDl, updateProxies, checkProxy, UserAgent
from multiprocessing import Pool
from os.path import dirname, abspath
from myfuc import readCsv, List
from requests import get
from time import sleep
from random import uniform
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
tmp = f'{pwd}/tmp'
html = f'{pwd}/html'
json = f'{pwd}/json'
orgList = 'orgList.csv'
orgListLeft = 'orgList_left.csv'
orgInfo = 'orgInfo.csv'
orgInfo_o = 'orgInfo_o.csv'

corpList = [
    ['technology', 'semiconductor'],
    ['technology', 'software'],
    ['technology', 'photoelectric'],
    ['technology', 'electroniccomponents'],
    ['technology', 'telecom'],
    ['searchJob', 'electronics'],
    ['manufacturing', 'manufacturing'],
    ['medicine', 'medicine'],
    ['financial', 'financial'],
    ['consumption', 'consumption'],
    ['others', 'others'],
]


def getList():
    for corp in corpList:
        res = get(f'https://www.104.com.tw/area/cj/foreign/{corp[0]}/category/{corp[1]}', headers=header)
        res.encoding = 'utf-8'
        with open(f'{html}/{corp[1]}.html', encoding='utf-8', mode='w+') as f:
            f.write(res.text)
        sleep(uniform(5, 10))


def getInfo():
    List([]).writeCsv(pwd, orgList)
    for corp in corpList:
        soup = bs(open(f'{html}/{corp[1]}.html', encoding='utf-8'), 'html.parser')
        List([[soup.select('.theme_tit > div')[0].text, c.select('img')[0]['title'].replace("/", "-"), c.select('a')[0]['href']] for c in soup.select('.company_detail')]).writeCsv(pwd, orgList, mode='a+')


def dl(urls):
    # updateProxies(tmp)
    # checkProxy([{'path': tmp, 'proxy': proxy} for proxy in readCsv(tmp, 'proxies.csv')])
    with Pool(7) as pool:
        pool.map(pageDl, [{'url': url[2], 'filePath': f'{html}/{url[1]}.html', 'proxyPath': tmp} for url in urls])


def getInfo2(corp):
    soup = bs(open(f'{html}/{corp[1]}.html', encoding='utf-8'), 'html.parser')
    intro = soup.select('.intro-table > div.col > div.row.mb-2')
    return [
        corp[1],
        corp[0],
        intro[0].select('div:nth-of-type(2) p')[0].text.replace(' ', ''),
        intro[1].select('div:nth-of-type(2) p')[0].text.replace(' ', ''),
        intro[1].select('div:nth-of-type(4) p')[0].text,
    ]


def main():
    with Pool(6) as pool:
        results = pool.map(getInfo2, readCsv(pwd, orgList))
    List([row for row in results]).writeCsv(pwd, orgInfo)


def test():
    res = []
    for corp in readCsv(pwd, orgList):
        try:
            open(f'{html}/{corp[1]}.html', encoding='utf-8')
        except FileNotFoundError as e:
            res.append([corp[0], corp[1], corp[2]])
    List(res).writeCsv(pwd, orgListLeft)


def dataC(df, col, reg, file):
    df[col] = df[col].str.replace(reg, '', regex=True)
    df.to_csv(f'{pwd}/{file}', index=False, encoding='utf-8-sig', mode='w+')
    return df


def getJson(keyword, output):
    sleep(0.1)
    try:
        res = get(f'https://data.gcis.nat.gov.tw/od/data/api/6BBA2268-1367-4B42-9CCA-BC17499EBE8C?$format=json&$filter=Company_Name%20like%20{keyword[4]}%20and%20Company_Status%20eq%2001&$skip=0&$top=50').json()
        List([[r['Company_Name'], r['Company_Location'], r['Responsible_Name'], '負責人', keyword[4], keyword[5], keyword[6], keyword[7], keyword[8], keyword[9], keyword[10], keyword[11], keyword[12]] for r in res]).writeCsv(pwd, output, mode='a+')
    except Exception as e:
        #List([['', '', '', '負責人', keyword[0], keyword[1], keyword[2], keyword[3], keyword[4], keyword[5], keyword[6], keyword[7], keyword[8]]]).writeCsv(pwd, output, mode='a+')
        List([['', '', '', '負責人', keyword[4], keyword[5], keyword[6], keyword[7], keyword[8], keyword[9], keyword[10], keyword[11], keyword[12]]]).writeCsv(pwd, output, mode='a+')


def main2(source, output):
    List([[
        '機構名稱',
        '地址',
        '姓名',
        '職稱',
        '機構名稱_2021',
        '地址_2021',
        '姓名_2021',
        '職稱_2021',
        '電話_2021',
        '產業',
        '產業類別',
        '產業描述',
        'year',
    ]]).writeCsv(pwd, output)
    for keyword in readCsv(pwd, source)[1:]:
        getJson(keyword, output)


if __name__ == '__main__':
    # dl(readCsv(pwd, orgList))
    # dataC(pd.read_csv(f'{pwd}/{orgInfo}', encoding='utf-8'), '機構名稱', r'(((\(|（).*(\)|）))|[A-Z]|[a-z]|.*集團_|\s|\.|,|_|-|台灣分公司|\'|。|\+|\&)*', 'orgInfo_n1.csv')
    # main2('orgInfo_n2.csv', orgInfo_o)
    # dataC(pd.read_csv(f'{pwd}/orgInfo_o_left.csv', encoding='utf-8'), '機構名稱_2021',r'(^(.*荷商|すき家、はま寿司台灣|三菱化學工程|佐丹奴香港商|台灣|味の素株式会社台灣|唐吉訶德台灣|國際半導體產業協會美商|外商|廣三{1}|德商|德商台灣|必勝客肯德基|愛爾蘭商|新加坡商|日商|日商台灣|東芝台灣|楊森藥廠|歐商|法商台灣|法商|法商迪卡儂台灣|法國特福|法國皇家|法國集團香水化粧品事業部香港商|法國高德美大藥廠香港商|澳洲商安科自動化|物業管理|瑞典伊維萊集團|瑞典商|瑞士商|美商亞洲分公司香港商|美商|美商東隆五金|美商永生臍帶血台灣|美商英屬蓋曼群島商|美威鮭魚台灣|英屬維京群島商|英屬蓋曼群島商|英屬開曼群島商|荷蘭商|菲商|薩摩亞商|象印家電|貝里斯商|達睿思國際傳播諮詢|韓商|香港商|高柏資本控股香港商|高誠公關萬博宣偉公關美商|高露潔好來牙膏牙刷產品系列|麥當勞授權發展商|香港商台灣)|(桃園分公司|聖羅蘭分公司|古馳|香港上海滙豐|碧歐斯|總公司|美商|台灣分公司|台北分公司)$|[a-z]|[A-Z]|\(|\)|（遠東）|商業|\s)', 'orgInfo_o_left_n1.csv')
    #main2('orgInfo_o_left_n1.csv', 'orgInfo_o_left_n2.csv')
    dataC(pd.read_csv(f'{pwd}/orgInfo_o_left_n3.csv', encoding='utf-8'), '機構名稱_2021', r'(^(凱度|服飾|西藥|史丹利|家樂福總公司|東隆五金{1}|比利時微電子研究中心_|永生臍帶血台灣|迪卡儂{1})|(2|在台辦事處)$|醱酵|台灣|臺灣|環匯)', 'orgInfo_o_left_n4.csv')
    main2('orgInfo_o_left_n4.csv', 'orgInfo_o_left_n5.csv')
