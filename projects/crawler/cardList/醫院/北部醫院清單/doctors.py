from pydoc import doc
import re
from time import sleep
from traceback import print_tb
from requests import get
from os.path import dirname, abspath
from bs4 import BeautifulSoup as bs
from myfuc import List, readCsv
from tryRequest import updateProxies, checkProxy, pageDl
from multiprocessing import Pool
from random import uniform

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
html = f'{pwd}/html'
tmp = f'{pwd}/tmp'

hospital = [
    ['https://wwwv.tsgh.ndmctsgh.edu.tw/doctable/191/26398', '三軍總醫院'],
]


def dl1(url):
    sleep(0.5)
    res = get(url[0])
    open(f'{html}/{url[1]}.html', encoding='utf-8', mode='w+').write(res.text)


def info1():
    soup = bs(open(f'{html}/三軍總醫院.html', encoding='utf-8'), 'html.parser')
    res = [[
        f"https://wwwv.tsgh.ndmctsgh.edu.tw{a['href']}",
        a['title']
    ] for i in range(2, 7) for a in soup.select(f'div.col-xs-12:nth-child({i}) > div:nth-child(2) > div > a')]
    List(res).writeCsv(pwd, 'links.csv')


def doctorsLinks():
    for a in readCsv(pwd, 'links.csv'):
        dl1([a[0], f'三軍總醫院-{a[1]}'])


def doctors():
    res = []
    for link in readCsv(pwd, 'links.csv'):
        soup = bs(open(f'{html}/三軍總醫院-{link[1]}.html', encoding='utf-8'), 'html.parser')
        res += [[f'https://wwwv.tsgh.ndmctsgh.edu.tw{a["href"]}', f'三軍總醫院-{a["title"]}'] for a in soup.select('.column.column-block.lg-txt > a')]
    List(res).writeCsv(pwd, 'doctorLinks.csv')


def doctorsInfoDl():
    # updateProxies(tmp)
    # checkProxy([{'path': tmp, 'proxy': proxy} for proxy in readCsv(tmp, 'proxies.csv')])
    with Pool(6) as pool:
        pool.map(pageDl, [{'url': link[0], 'filePath': f'{html}/{link[1]}.html', 'proxyPath': tmp} for link in readCsv(pwd, 'doctorLinks.csv')])


def depDl_vghtpe():
    soup = bs(open(f'{html}/台北榮總/科部清單.html', encoding='utf-8'), 'html.parser')
    List([[a.text, a['href']] for a in soup.select('td a')]).writeCsv(f'{html}/台北榮總', '台北榮總科部清單.csv', mode='w+')


def doctor_vghtpe():
    soup = bs(open(f'{html}/台北榮總/doctors.html', encoding='utf-8'), 'html.parser')
    List([[re.sub('\(.*\)', '', card.select('#name')[0].text.replace('\n', '').replace(' ', '')) if '主任' in card.select('#title')[0].text.replace('\n', '').replace(' ', '') else ''] for card in soup.select('#DIV2')]).writeCsv(f'{html}/台北榮總', '醫師名單.csv')


def doctorList_femh():
    soup = bs(open(f'{html}/亞東紀念醫院/doctors.html', encoding='utf-8'), 'html.parser')
    List([[info.text.replace(' ', ''), re.sub('\.{2}', 'https://www.femh.org.tw', info['href'])] for info in soup.select('.arWebFont a')]).writeCsv(f'{html}/亞東紀念醫院', 'doctorList.csv')


def info_femh(doctor):
    soup = bs(open(f'{html}/亞東紀念醫院/{doctor[0]}.html', encoding='utf-8'), 'html.parser').select('div.text:nth-child(2) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(2) li')
    return [[doctor[0], re.sub('(亞東紀念醫院|\s)*', '', li.text)] for li in soup if re.search('(科主任|部主任|院長)$', li.text)]


def doctors_femh():
    List([['hospital', 'name', 'title', 'address', '電話', 'email', '級別']]).writeCsv(f'{html}/亞東紀念醫院', 'doctors-亞東紀念醫院.csv')
    with Pool(6) as pool:
        res = pool.map(info_femh, readCsv(f'{html}/亞東紀念醫院', 'doctorList.csv'))
    res = [['醫療財團法人徐元智先生醫藥基金會亞東紀念醫院', r[0], r[1], '新北市板橋區南雅南路二段21號及高爾富路300號', '(02)  89667000', '', '醫學中心'] for r in list(filter(lambda d: d != [], [row for rows in res for row in rows]))]
    List(res).writeCsv(f'{html}/亞東紀念醫院', 'doctors-亞東紀念醫院.csv', mode='a+')


def doctorList_cgmh():
    soup = bs(open(f'{html}/林口長庚/dep-林口長庚.html', encoding='utf-8'), 'html.parser')
    List([[re.sub('\n*', '', a.text), f"https://www.cgmh.org.tw{a['href']}"] for a in soup.select('.ul-reset.innerlist.fz-17 li a')]).writeCsv(f'{html}/林口長庚', 'depList.csv')


def doctors_cgmh(dep):
    soup = bs(open(f'{html}/林口長庚/doctors/{dep[0]}.html', encoding='utf-8'), 'html.parser')
    return [[
        re.sub('(\n|\s)*', '', tr.select('td')[0].text),
        tr.select('td')[1].text,
    ] for tr in soup.select('.layout__table-main tr')[1:] if re.search('(科主任|部主任|院長)$', tr.select('td')[1].text)]


def doctorList_tzuchi(dep):
    soup = bs(open(f'{html}/台北慈濟/depList/{dep[0]}.html', encoding='utf-8'), 'html.parser')
    return [[re.sub(r'(\t|\n)*', '', doctor.select('h4')[0].text), doctor.select('a')[0]['href']] for doctor in soup.select('article.elementor-post')]


def doctors_tzuchi(doctor):
    soup = bs(open(f'{html}/台北慈濟/doctors/{doctor[0]}.html', encoding='utf-8'), 'html.parser')
    print(soup.select('div.elementor-element.elementor-widget.elementor-widget-text-editor')[0].text)
    return


class HospitalSite:
    def __init__(self, hospital) -> None:
        self.hospital = hospital

    def doctorList(self):
        pass


if __name__ == "__main__":
    doctors_tzuchi(readCsv(f'{html}/台北慈濟', 'doctorList.csv')[0])
    '''
    with Pool(8) as pool:
        results = pool.map(doctorList_tzuchi, readCsv(f'{html}/台北慈濟', 'depList.csv'))
    List([row for group in results for row in group]).writeCsv(f'{html}/台北慈濟', 'doctorList.csv')
    '''
    # updateProxies(tmp)
    # checkProxy([{'path': tmp, 'proxy': proxy} for proxy in readCsv(tmp, 'proxies.csv')])
    '''with Pool(8) as pool:
        pool.map(pageDl, [{'url': f'https://taipei.tzuchi.com.tw/{link[0]}/', 'filePath': f'{html}/台北慈濟/doctors/{link[0]}.html', 'proxyPath': tmp} for link in readCsv(f'{html}/台北慈濟', 'doctorList.csv')])'''
