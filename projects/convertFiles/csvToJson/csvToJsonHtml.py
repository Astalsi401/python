import os
from csv import writer, reader
from json import dump

#pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


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
    name = name.replace('.csv', '.json')
    if not os.path.isdir(f'{path}'):
        os.makedirs(f'{path}')
    with open(f'{path}/{name}', mode, encoding=encoding) as f:
        dump(json, f, ensure_ascii=False)
        print(f'{path}/{name} saved!')


def writeHtml(path, data, name):
    '''list to html table'''
    if not os.path.isdir(f'{path}'):
        os.makedirs(f'{path}')
    htmlTable = '<table>'
    for row in data:
        htmlTable += '<tr>'
        for c in row:
            htmlTable += f'<td>{c}</td>'
        htmlTable += '</tr>'
    htmlTable += '</table>'
    with open(f'{path}/{name}.html', mode='w+') as f:
        f.write(htmlTable)


files = [
    "生醫興櫃營收Top20.csv",
    "生醫上市營收Top20.csv",
    "生醫上櫃營收Top20.csv",
]

for f in files:
    name = f.replace('.csv', '')
    writeJson('D:/Documents/work/indust/seasonReport/csv/json', convertToJson(readCsv('D:/Documents/work/indust/seasonReport/csv', f)), f'{name}.json')
'''for name in getFilesName(f'{pwd}/csv', 'csv'):
    writeJson(f'D:/Documents/work/htmlfix/hotel', convertToJson(readCsv(f'D:/Documents/work/htmlfix/hotel', f'hotel.csv')), f'hotel')
    #writeHtml(readCsv(f'{pwd}/csv', name), name.replace('.csv', ''))
'''
