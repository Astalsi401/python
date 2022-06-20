from myfuc import readCsv, writeCsv, getFilesName

pwd = 'D:/Documents/work/indust/seasonReport/csv'

fileNames = getFilesName(pwd, 'csv')
for w in fileNames:
    wn = w.replace('.csv', '')
    writeCsv(pwd, f'{wn}_n.csv', readCsv(f'{pwd}', f'{w}'))
