from os.path import dirname, abspath
from myfuc import readCsv
from pyzbar.pyzbar import decode
import qrcode
import cv2


pwd = dirname(abspath(__file__)).replace('\\', '/')
qrcodePath = f'{pwd}/qrcode'
language = ['tc', 'en']


def createQrcode(name, data):
    '''
    data=要轉換為qrcode的資料
    fileName=qrcode圖檔名稱
    size=圖片尺寸
    '''
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(name)
    print(f'name: {name}\rdata:{data}\rqrcode:{name}')


def readQrcode(path):
    image = cv2.imread(path, 0)
    barcodes = decode(image)
    return barcodes[0].data.decode("utf-8")


def checkLink(path, link):
    return link if link != readQrcode(path) else True


def main():
    for lg in language:
        for link in readCsv(f'{pwd}', f'data_{lg}.csv'):
            createQrcode(f'{qrcodePath}/{lg}/{link[0]}.png', link[1])


def main2():
    check = [[link[1], checkLink(f'{qrcodePath}/{lg}/{link[0]}.png', link[1])] for lg in language for link in readCsv(f'{pwd}', f'data_{lg}.csv')]
    print(check)


if __name__ == '__main__':
    main2()
