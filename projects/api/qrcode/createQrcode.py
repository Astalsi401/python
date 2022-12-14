from os.path import dirname, abspath, exists
from os import makedirs
from pyzbar.pyzbar import decode
import qrcode
import cv2
import pandas as pd
import re


pwd = dirname(abspath(__file__)).replace('\\', '/')
qrcodePath = f'{pwd}/qrcode'
qrcodeCatPath = f'{pwd}/catPath'
language = ['tc', 'en']


def readCsv(path):
    return pd.read_csv(path, header=None).values.tolist()


def mergeData():
    links = pd.read_excel(f'{pwd}/links.xlsx', names=['公司名稱(中文)', '公司名稱(英文)', '企業頁面連結(中文)+參數', '企業頁面連結(英文)+參數'])
    cat = pd.concat([pd.read_excel(f'{pwd}/智慧醫院.xlsx', names=['類別', '公司名稱']), pd.read_excel(f'{pwd}/精準檢測.xlsx', names=['類別', '公司名稱'])], ignore_index=True).drop_duplicates(subset=['公司名稱'], ignore_index=True)
    res = links.merge(cat, left_on='公司名稱(中文)', right_on='公司名稱', how='left').dropna(axis=0, subset=['公司名稱'])
    return {'tc': res[['公司名稱(中文)', '類別', '企業頁面連結(中文)+參數']], 'en': res[['公司名稱(英文)', '類別', '企業頁面連結(英文)+參數']]}


def createQrcode(path, data):
    '''
    path=qrcode儲存路徑
    data=要轉換為qrcode的資料
    '''
    path = re.sub(r'\t', '', path)
    p = re.sub(r'\/[^\/]*png$', '', path)
    if not exists(p):
        makedirs(p)
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    qr.make_image().save(path)


def readQrcode(path):
    image = cv2.imread(path, 0)
    barcodes = decode(image)
    return barcodes[0].data.decode("utf-8")


def checkLink(path, link):
    return link if link != readQrcode(re.sub(r'\t', '', path)) else True


def main():
    for lg in language:
        for link in readCsv(f'{pwd}/data_{lg}.csv'):
            createQrcode(f'{qrcodePath}/{lg}/{link[0]}.png', link[1])


def check():
    check = [[link[2], checkLink(f'{qrcodeCatPath}/{lg}/{link[1]}/{link[0]}.png', link[2])] for lg in language for link in mergeData()[lg].values.tolist()]
    checkRes = list(filter(lambda row: row[1] == False, check))
    print(checkRes if checkRes != [] else 'No difference')


def main2(path: str, df: dict):
    for lg in language:
        for link in df[lg].values.tolist():
            createQrcode(f'{path}/{lg}/{link[0]}.png', link[2])


def addNew(date, ext='csv'):
    df = pd.read_csv(f'{pwd}/addNew{date}.csv') if ext == 'csv' else pd.read_excel(f'{pwd}/addNew{date}.xlsx')
    df['類別'] = '新增'
    df['公司名稱(中文)'] = df['公司名稱(中文)'].replace(regex=r'/', value='')
    df['公司名稱(英文)'] = df['公司名稱(英文)'].replace(regex=r'/', value='')
    main2(f'{pwd}/addNew/{date}', {'tc': df[['公司名稱(中文)', '類別', '企業頁面連結(中文)+參數']], 'en': df[['公司名稱(英文)', '類別', '企業頁面連結(英文)+參數']]})


if __name__ == '__main__':
    addNew('1123', 'xlsx')
