from myfuc import MyPdf, Combine
from os import chdir
from os.path import dirname, abspath
import pandas as pd


chdir(dirname(abspath(__file__)))
pd.set_option('display.max.columns', None)


def main():
    for w1, w2 in [['(大專學生)產業見習證明', '產業見習']]:
        df = pd.read_excel('secret/excel/2022時數證明/時數計算_學生個人.xlsx', sheet_name=w2)
        MyPdf(df, pdfPath=f'secret/合併列印/2022時數證明/{w1}.pdf').split(1, f'secret/pdf/2022時數證明/{w2}', ['編號', '姓名', 'date'], folder='編號')


def main2():
    #writer = pd.ExcelWriter('secret/時數計算_學生個人_url.xlsx', engine='xlsxwriter')
    # writer.close()
    excelPath = 'secret/excel/2022時數證明'
    for w, n in [['產業見習', 9], ['高中生', 12]]:
        url = pd.concat([pd.read_excel(f'{excelPath}/時數證明_url.xlsx', sheet_name=f'{w}p{i}') for i in range(1, n)])
        profile = pd.read_excel(f'{excelPath}/時數計算_學生個人.xlsx', sheet_name=w, usecols=['編號', '姓名', 'date', '電子郵件地址'])
        profile['編號'] = profile['編號'].str.replace('|', '', regex=False)
        edmList = Combine(profile, url, w).merge('編號', 'inner')
        edmList[['出生西元年', '自訂欄位3']] = ''
        edmList[['電子郵件地址', '姓名', '出生西元年', 'URL', '編號', '自訂欄位3']].to_csv(f'{excelPath}/{w}_時數證明寄送.csv', encoding='utf-8', index=False, header=False)


def main3():
    df = pd.read_excel('secret/excel/2022時數證明/時數計算_教師領團-高中生-剩餘.xlsx')
    MyPdf(df, pdfPath=f'secret/合併列印/2022時數證明/高中_額外.pdf').split(1, f'secret/pdf/2022時數證明/教師領團-高中生-剩餘', ['編號', '姓名', 'date'], folder='電子郵件地址', limit=float('inf'))


def main4():
    df = pd.concat([pd.read_excel('secret/excel/2022時數證明/時數證明_url.xlsx', sheet_name=f'大專團報p{i}', usecols=['Name', 'Type', 'URL']) for i in range(1, 6)]).query('Type == "Folder"')
    df = df.merge(pd.read_excel('secret/excel/2022時數證明/時數計算_教師領團-大專生-寄送名單.xlsx'), how='right', left_on='Name', right_on='電子郵件地址')
    df[['編號', '姓名', '學校', '手機', '電子郵件地址', 'date', '簽到', '簽退', '時數', 'URL']].to_excel('secret/excel/2022時數證明/大專生_教師領團_時數證明寄送.xlsx', index=False)


if __name__ == '__main__':
    main3()
    # main4()
