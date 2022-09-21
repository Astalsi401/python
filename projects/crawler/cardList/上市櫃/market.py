from calendar import c
import pandas as pd
import re
from os.path import dirname, abspath

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))


def info(market):
    df = pd.read_csv(f'{pwd}/{market}.csv')
    df = pd.DataFrame(df, columns=['公司名稱', '產業類別', '住址', '董事長', '總經理', '總機電話', '電子郵件信箱'])
    cat = ['生技醫療', '半導體', '光電', '電機機械', '電子零組件', '電腦週邊', '資訊', '通訊網路', '農業科技', '食品', '化學', '金融', '橡膠', '塑膠', '紡織', '紙類', '通路']
    df = df[df['產業類別'].str.contains('|'.join(cat), na=False)]
    df1 = pd.DataFrame(df, columns=['公司名稱', '住址', '董事長', '總機電話', '電子郵件信箱', '產業類別'])
    df1['職稱'] = '董事長'
    df1 = df1.rename(columns={'董事長': '姓名'})
    df2 = pd.DataFrame(df, columns=['公司名稱', '住址', '總經理', '總機電話', '電子郵件信箱', '產業類別'])
    df2['職稱'] = '總經理'
    df2 = df2.rename(columns={'總經理': '姓名'})
    df = pd.concat([df1, df2], ignore_index=True)
    df['市場'] = market
    df['其他來源分類'] = ''
    df = pd.DataFrame(df, columns=['公司名稱', '住址', '姓名', '職稱', '總機電話', '電子郵件信箱', '市場', '產業類別', '其他來源分類'])
    return df


def main():
    res = pd.concat([info(market) for market in ['上市', '上櫃', '興櫃']], ignore_index=True)
    res.to_csv(f'{pwd}/orgInfo.csv', encoding='utf-8-sig', index=False)
    return res


print(main())
