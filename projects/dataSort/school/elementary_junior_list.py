import pandas as pd
from os.path import dirname, abspath
from requests import get
from tryRequest import pageDl, checkProxy, updateProxies

pwd = dirname(abspath(__file__)).replace('\\', '/')
html = f'{pwd}/html'
tmp = f'{pwd}/tmp'


def search(key):
    pageDl(link={'url': f'https://www.google.com/search?q={key}', 'filePath': html, 'proxyPath': tmp})


def main():
    df = pd.concat([pd.read_csv(f'{pwd}/csv/{f}.csv', usecols=['學校名稱', '縣市名稱']) for f in ['ac', 'aj_new', 'e1_new', 'j1_new', ]]).query('`縣市名稱`.str.match(".*新北市.*|.*臺北市.*")')
    print(df)


if __name__ == '__main__':
    # updateProxies(tmp)
    main()
    # print(pd.read_csv())
    # checkProxy([{'path': tmp, 'proxy': row} for row in ])
