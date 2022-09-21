import pandas as pd
import re
from os.path import dirname, abspath

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))


def main():
    df = pd.read_csv(f'{pwd}/OfficesInROC.csv')
    df = pd.DataFrame(df, columns=['館名(中文)', '地址(中文)', '姓名(英文)', '電話', '電子郵件'])
    df['職稱'] = ''
    df['分類'] = '駐台辦事處'
    df = pd.DataFrame(df, columns=['館名(中文)', '地址(中文)', '姓名(英文)', '職稱', '電話', '電子郵件', '分類'])
    df.to_csv(f'{pwd}/officeInROC.csv', index=False, encoding='utf-8-sig')
    return df


print(main())
