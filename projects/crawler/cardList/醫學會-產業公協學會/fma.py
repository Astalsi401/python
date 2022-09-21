import pandas as pd
import re
from os.path import dirname, abspath

pwd = re.sub('/py$', '', dirname(abspath(__file__)).replace('\\', '/'))


def fm(df, varList):
    for v in varList:
        df[v] = df[v].str.replace('台', '臺')
        df[v] = df[v].str.replace('（', '(')
        df[v] = df[v].str.replace(' ', '')
    return df


def new():
    df = pd.read_csv(f'{pwd}/全國社會團體名冊-結構化.csv')
    new = pd.DataFrame(df, columns=['NAME', 'ADDRESS', 'CHAIRMAN'])
    new = fm(new, ['NAME', 'ADDRESS'])
    new['ADDRESS'] = new['ADDRESS'].fillna('')
    new['ADDRESS'] = ['('.join([string for string in strings.split('(') if '備查' not in string]) for strings in new['ADDRESS'].to_list()]
    return new


def old(sheet, cat, cat_f):
    df = pd.read_excel(f'{pwd}/2021邀請卡寄送名單.xlsx', sheet_name=sheet)
    old = pd.DataFrame(df, columns=['機構名稱', '機構地址', '代表人姓名', cat])
    old = old[old[cat].str.contains('|'.join([cat_f]), na=False)]
    old = fm(old, ['機構名稱', '機構地址'])
    old['職稱'] = '理事長'
    old['電話'] = ''
    old['email'] = ''
    old['子類別'] = cat_f
    return old


def main(old):
    res = old.merge(new(), left_on='機構名稱', right_on='NAME', how='left')
    for v in [['NAME', '代表人姓名'], ['ADDRESS', '機構地址'], ['CHAIRMAN', '代表人姓名']]:
        res[v[0]] = res[v[0]].fillna(res[v[1]])
    res = pd.DataFrame(res, columns=['NAME', 'ADDRESS', 'CHAIRMAN', '職稱', '電話', 'email', '子類別'])
    res.to_csv(f'{pwd}/orgInfo-ind.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    #main(old('醫界 (9783)', '分類', '醫學會'))
    main(old('駐台.產業(7342)', '其他來源', '產業公協學會'))
