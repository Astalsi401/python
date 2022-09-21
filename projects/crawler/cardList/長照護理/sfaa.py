import re
import pandas as pd
from os.path import dirname, abspath

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))
cities = ['臺北市', '新北市', '基隆市', '新竹市', '桃園市', '新竹縣', '宜蘭縣']


def main():
    dfs = []
    for city in cities:
        print(city)
        df = pd.read_excel(f'{pwd}/File_182847.xlsx', sheet_name=city, skiprows=1)
        df = pd.DataFrame(df, columns=['編號', '機構名稱', '地址', '負責人', '電話', '收容對象'])
        try:
            df = df[~df['編號'].str.contains('|'.join(['歇業']), na=False)]
            df = df[~df['編號'].str.contains('|'.join(['裁撤']), na=False)]
        except AttributeError:
            pass
        df = df.dropna(subset=['機構名稱'])
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


if __name__ == '__main__':
    main().to_csv(f'{pwd}/sfaa.csv', index=False, encoding='utf-8-sig')
