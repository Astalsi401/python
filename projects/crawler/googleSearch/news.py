from requests import get
from bs4 import BeautifulSoup as bs
from os import chdir
from os.path import dirname, abspath
from time import sleep
from myfuc import List
import pandas as pd
import re

chdir(dirname(abspath(__file__)))
results = 'results.csv'


def htmlDl():
    for i, page in enumerate(range(0, 190, 10)):
        open(f'html/page{i}.html', mode='w+', encoding='utf-8').write(get(f'https://www.google.com/search?q=2022台灣醫療科技展&tbas=0&tbs=cdr:1,cd_min:1/1/2022,cd_max:12/19/2022,sbd:1&tbm=nws&start={page}').text)
        sleep(10)


def getNews():

    List([['標題', '摘要', '連結']]).writeCsv(results, mode='w+')
    for i in range(0, 19):
        soup = bs(open(f'html/page{i}.html', mode='r'), 'html.parser')
        List([[e.select('a > div')[0].text, e.select('a > div')[1].text, e.select('a')[0]['href']] for e in soup.select('div#main > div')[3:]]).writeCsv(results, mode='a+')


def clean():
    df = pd.read_csv(results).replace(r'(/url\?q=)|\n', '', regex=True)
    reg = r'(台|臺)灣醫療科技展'
    df = df[(df['標題'].str.contains(reg, regex=True) == True) | (df['摘要'].str.contains(reg, regex=True) == True)]
    df.to_csv(f'new_{results}', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    clean()
