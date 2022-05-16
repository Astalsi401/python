import os
from csv import writer, reader
from json import dump


def writeCsv(path, name, data, mode='w+'):
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(f'{path}/{name}', mode=f'{mode}', encoding='utf-8-sig', newline='') as f:
        for a in data:
            writer(f).writerow(a)
    print(f'{path}/{name} saved!')


def readCsv(path, name):
    a = []
    with open(f'{path}/{name}', mode='r', encoding='utf-8-sig', newline='') as f:
        b = reader(f)
        for c in b:
            a.append(c)
    return a


def getFilesName(path, ext=None):
    if ext == None:
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    else:
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f'.{ext}' in f]


def convertToJson(data):
    json = []
    for a in data:
        i = 0
        b = {}
        for c in a:
            b[f'row{i}'] = c
            i += 1
        json.append(b)
    return json


def writeJson(path, json, name, mode='w+', encoding='utf-8-sig'):
    if not os.path.isdir(f'{path}'):
        os.makedirs(f'{path}')
    name = name.replace('.csv', '.json')
    with open(f'{path}/{name}', mode, encoding=encoding) as f:
        dump(json, f, ensure_ascii=False)
        print(f'{path}/{name} saved!')


pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
for name in getFilesName(f'{pwd}/csv', 'csv'):
    writeJson(f'{pwd}/json', convertToJson(readCsv(f'{pwd}/csv', f'{name}')), f'{name}')
