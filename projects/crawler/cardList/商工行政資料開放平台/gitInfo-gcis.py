import re
from os.path import dirname, abspath
from time import sleep
from requests import get
from myfuc import readCsv, List

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
json = f'{pwd}/json'
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


def getJson(keyword):
    sleep(0.1)
    try:
        res = get(f'https://data.gcis.nat.gov.tw/od/data/api/6BBA2268-1367-4B42-9CCA-BC17499EBE8C?$format=json&$filter=Company_Name%20like%20{keyword[0]}%20and%20Company_Status%20eq%2001&$skip=0&$top=50').json()
        List([[r['Company_Name'], r['Company_Location'], r['Responsible_Name'], '負責人', keyword[4], keyword[5], keyword[6], keyword[7], keyword[8]] for r in res]).writeCsv(pwd, 'orgInfo_o.csv', mode='a+')
    except Exception as e:
        print(e)


def main():
    List(colname).writeCsv(pwd, 'orgInfo_o.csv')
    for keyword in readCsv(pwd, 'noInfo.csv')[1:]:
        getJson(keyword)


if __name__ == '__main__':
    main()
