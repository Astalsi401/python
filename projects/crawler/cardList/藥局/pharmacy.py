import pandas as pd
import re
from os.path import dirname, abspath

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
cities = ['臺北市', '新北市', '基隆市', '新竹市', '桃園市', '新竹縣', '宜蘭縣']

df = pd.read_csv(f'{pwd}/35_2.csv')
df = pd.DataFrame(df, columns=['機構名稱', '地址縣市別', '地址鄉鎮市區', '地址街道巷弄號', '負責人姓名', '電話'])
df = df[df['地址縣市別'].str.contains('|'.join(cities))]
df['地址'] = df['地址縣市別'] + df['地址鄉鎮市區'] + df['地址街道巷弄號']
df['職稱'] = '負責人'
df['email'] = ''
df['子類別'] = '藥局'
df = pd.DataFrame(df, columns=['機構名稱', '地址', '負責人姓名', '職稱', '電話', 'email', '子類別'])
print(df)
df.to_csv(f'{pwd}/orfInfo.csv', index=False, encoding='utf-8-sig')
