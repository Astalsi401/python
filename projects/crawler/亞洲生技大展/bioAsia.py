from requests import get
from tryRequest import updateProxies, checkProxy, pageDl
from myfuc import List, readCsv
from os.path import dirname, abspath, isfile
from os import chdir
from time import sleep
from multiprocessing import Pool
from bs4 import BeautifulSoup as bs
import re

chdir(dirname(abspath(__file__)))
tmp = '.tmp'
html = 'html'


def main():
    for i in range(1, 21):
        'https://expo.bioasiataiwan.com/visitorExhibitor.asp?page=2'
        res = get(f'https://expo.bioasiataiwan.com/visitorExhibitor.asp?page={i}')
        res.encoding = 'utf-8'
        open(f'{html}/page{i}.html', mode='w+', encoding='utf-8').write(res.text)
        sleep(15)


def dl():
    # updateProxies(tmp)
    #checkProxy([{'path': tmp, 'proxy': proxy} for proxy in readCsv(tmp, 'proxies.csv')])
    urls = readCsv('urls_bioAsia.csv')
    urls = [[name, url] for name, url in urls if isfile(f'{html}/{name}.html') == False]
    with Pool(8) as pool:
        pool.map(pageDl, [{'url': f'https://expo.bioasiataiwan.com/{url}', 'filePath': f'{html}/{name}.html', 'proxyPath': tmp} for name, url in urls])


def select_n(soup, selector):
    try:
        return soup.select(selector)[0].text
    except IndexError:
        return ''


def bioAsia_urls():
    List([]).writeCsv('urls_bioAsia.csv', mode='w+')
    for i in range(1, 21):
        lis = bs(open(f'{html}/page{i}.html', mode='r'), 'html.parser').select('.product > li')
        List([[re.sub(r'\/|\?|\|', '', li.select('h4 a')[0].text), li.select('div:nth-child(1) > a')[0]['href']] for li in lis]).writeCsv('urls_bioAsia.csv', mode='a+')


def bioAsia_results():
    List([['公司名稱', '分類', '簡介', '網址']]).writeCsv('results_bioAsia.csv', mode='w+')
    for name, url in readCsv('urls_bioAsia.csv'):
        print(name, f'https://expo.bioasiataiwan.com/{url}')
        html_text = open(f'{html}/{name}.html', mode='r').read()
        soup = bs(html_text, 'html.parser').select('#right')[0]
        category = select_n(soup, 'p:nth-child(4) > a')
        link = select_n(soup, 'p:nth-child(6) > a')
        text = re.sub(r'\n|\s\s', '', html_text)
        intro = re.search(r'<h3>廠商介紹</h3>(.*?<p class="lightLine">&nbsp;</p>)', text)
        intro = re.sub(r'廠商介紹 ', '', bs(intro.group(), 'html.parser').text) if intro else ''
        List([[name, category, intro, link]]).writeCsv('results_bioAsia.csv', mode='a+')


if __name__ == '__main__':
    bioAsia_results()
