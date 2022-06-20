from myfuc import readCsv, writeCsv
import os
import re


pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
files = [
    '生醫上市營收Top20',
    '生醫上市櫃營收Top20',
    '生醫上櫃營收Top20',
    '生醫興櫃營收Top20'
]


def main():
    for f in files:
        data = [readCsv(f'{pwd}/csv', f'{f}.csv')[0]]
        for row in readCsv(f'{pwd}/csv', f'{f}.csv'):
            for eng in readCsv(f'{pwd}/csv', 'stockEng.csv'):
                row[1].replace('-KY', '')
                if row[1] == re.findall(re.compile(r'[(](.*?)[)]', re.S), eng[0])[0]:
                    row.append(eng[0])
                    data.append(row)
        writeCsv(f'{pwd}/csv', f'{f}_eng.csv', data, enc='utf-8')


main()
