from bs4 import BeautifulSoup as bs
from os import chdir
from os.path import dirname, abspath
from myfuc import List
import re
import pandas as pd

chdir(dirname(abspath(__file__)))


def main():
    soup = bs(open('bigGo.html', encoding='utf-8', mode='r'), 'html.parser')
    p = r'\n|\s|\$|,'
    f = '掃描器比價.csv'
    List([['品名', '價格', '來源', '連結']]).writeCsv(f, mode='w+')
    List([[
        re.sub(p, '', card.select('.title a')[0].text),
        re.sub(p, '', card.select('.price')[0].text),
        re.sub(p, '', card.select('.store-name-wrap')[0].text),
        f'https://biggo.com.tw{card.select(".title a")[0]["href"]}'] for card in soup.select('.cardview-wrap .desc')]).writeCsv(f, mode='a+')
    pd.set_option('display.max.columns', None)
    df = pd.read_csv(f).sort_values(by='價格')
    df = df.drop(df[(df.價格 < 10000) | (df.價格 > 18000)].index)
    df.to_csv(f, index=False)


main()
