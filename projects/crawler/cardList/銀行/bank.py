import pandas as pd
import re
from os.path import dirname, abspath
from myfuc import List

pwd = re.sub(r'\\', '/', dirname(abspath(__file__)))


def main1():
    df = pd.read_csv(f'{pwd}/bankno.csv', encoding='utf-8', sep='\t')
    df.columns = [re.sub(r'=|"', '', col) for col in df.columns.to_list()]
    for col in df.columns.to_list():
        df[col] = df[col].str.replace(r'=|"', '', regex=True)
    df = df[['機構名稱', '地址', '電話', '負責人']]
    df = df.merge(pd.DataFrame([{'負責人': ''}]), how='left', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])
    df = df[df['地址'].str.contains(r'臺北市|台北市', regex=True, na=False)]
    df.to_csv(f'{pwd}/bankno_n.csv', encoding='utf-8-sig', index=False)


def main2():
    res = []
    for row in open(f'{pwd}/台北市銀行.csv').readlines():
        if row != ',\n':
            res.append(re.sub(r'^,+|,+$', '', re.sub(r'\s+', ',', row)).split(','))
    List(res).writeCsv(pwd, 'taipeiBank.csv')


if __name__ == '__main__':
    main1()
