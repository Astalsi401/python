from bs4 import BeautifulSoup
import codecs
import random
import requests
import sys
import time

pwd = 'D:/Documents/Data/pyinstall/companyDataBase'

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
}
df = []
page = ['']
cities = ['基隆市', '台北市', '新北市', '桃園市', '新竹縣', '新竹市', '苗栗縣', '台中市', '彰化縣', '南投縣', '雲林縣',
          '嘉義市', '嘉義縣', '台南市', '高雄市', '屏東縣', '宜蘭縣', '花蓮縣', '台東縣', '澎湖縣', '金門縣', '連江縣']
for i in range(2, 301):
    page.append(f'-{i}')

with open(f'{pwd}/txtFile.txt', 'w') as txtFile:
    for city in cities:
        for i in page:
            url = f'https://alltwcompany.com/a1-{city}{i}.html'
            res = requests.get(url, headers=headers)
            res.encoding = 'utf-8'
            res.text
            soup = BeautifulSoup(res.text, 'lxml')
            links = soup.select('div.store_list')[1].select('a')
            for j in links:
                company = j.get('title')
                companyLink = j.get('href')
                df.append(f'{companyLink}')
                txtFile.write(f'{companyLink}\n')
                print(f'page: {i}  title: {company}')
            sleeptime = random.uniform(5, 10)
            print(f'wait {sleeptime} sec...')
            time.sleep(sleeptime)
        print(df)
