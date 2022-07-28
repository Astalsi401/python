from myfuc import readCsv
siteList = [(s[0], None)[s[0] != ''] for s in readCsv(pwd, 'siteList.csv')]
