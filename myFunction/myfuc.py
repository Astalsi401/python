import os
from csv import writer, reader
from datetime import date
from xml.etree.ElementTree import tostring


def writeCsv(path, name, data, mode='w+'):
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(f'{path}/{name}', mode=f'{mode}', encoding='utf-8-sig', newline='') as f:
        for a in data:
            writer(f).writerow(a)
    print(f'{name} saved!')


def readCsv(path, name):
    a = []
    with open(f'{path}/{name}', mode='r', encoding='utf-8-sig', newline='') as f:
        b = reader(f)
        for c in b:
            a.append(c)
    return a


def yearsCalc(yearsAgo=0):
    '''列出最近3年年份'''
    a = []
    for b in range(0, yearsAgo):
        a.append(str(date.today().year - b))
    return a
