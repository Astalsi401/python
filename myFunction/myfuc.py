import os
import requests
from csv import writer, reader
from datetime import date
from openpyxl import load_workbook
from time import sleep
import pandas as pd


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


def getXlsxSheets(path, name):
    wb = load_workbook(f'{path}/{name}.xlsx')
    sheetnames = wb.get_sheet_names()
    with open(f'{path}/{name}_sheetname.txt', 'w', encoding='UTF-8-sig') as f:
        for b in sheetnames:
            f.write(f'{b}\n')
    print(f'{name}_sheetname.txt saved')


def yearsCalc(yearsAgo=0):
    '''列出最近3年年份'''
    a = []
    for b in range(0, yearsAgo):
        a.append(str(date.today().year - b))
    return a
