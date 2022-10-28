from operator import mod
import re
from typing import List
from bs4 import BeautifulSoup as bs
from os.path import dirname, abspath
from myfuc import List

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))


def main():
    soup = bs(open(f'{pwd}/診所美容醫學品質認證通過之醫療機構.html', encoding='utf-8'), 'html.parser')
    List([[tr.select('td:nth-of-type(2) a')[0].text.replace('\n', ''), tr.select('td:nth-of-type(3) > div')[0].text] for tr in soup.select('tr')]).writeCsv(f'{pwd}', 'orgInfo.csv')


main()
