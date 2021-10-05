import urllib3
from bs4 import BeautifulSoup
http = urllib3.PoolManager()
url = 'https://web.cw.com.tw/2020-taiwan-presidential-election/data-analysis/?areacode=63000010-002&emoji=smile'
response = http.request('GET', url)
soup = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
pol2018 = soup.select('.databox__title')
print(pol2018)