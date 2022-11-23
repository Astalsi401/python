import pandas as pd
import numpy as np
from os.path import dirname, abspath
from random import sample, seed

pwd = dirname(abspath(__file__)).replace('\\', '/')


def sameLen(colname, row: list, l: int):
    i = 1
    while len(row) < l:
        row.append(f'{colname}_null_{i}')
        i += 1
    return row


def schedule(df):
    time_num = 17
    twCorp = df.groupby(['台灣公司名稱']).size().reset_index(name='num')
    df = df.merge(twCorp, left_on='台灣公司名稱', right_on='台灣公司名稱').sort_values('num', ascending=True, ignore_index=True)
    foreign_list = []
    for f in df['單位名稱'].values.tolist():
        if f not in foreign_list:
            foreign_list.append(f)
    foreign_num = len(foreign_list)
    foreign = {f: sameLen(f, list(set([cell[0] for cell in df.query(f'單位名稱 == "{f}"')[['台灣公司名稱']].values.tolist()])), time_num) for f in foreign_list}
    matrix = np.array([sample(foreign[foreign_list[0]], time_num)])
    matrix_n = np.append(matrix, [sample(foreign[foreign_list[1]], time_num)], axis=0)
    col_count = 0
    col_limit = 200000
    for c in range(1, foreign_num):
        col_count = 0
        while 1:
            matrix_n = np.append(matrix, [sample(foreign[foreign_list[c]], time_num)], axis=0)
            cols = [matrix_n[:, col] for col in range(time_num)]
            cols_set = [set(col) for col in cols]
            col_count += 1
            col_len = [len(col) for col in cols]
            cols_set_len = [len(col) for col in cols_set]
            if col_len == cols_set_len or col_count >= col_limit:
                matrix = matrix_n
                print(f'{foreign_list[c]} (col {c}) calc {col_count} times')
                col_count = 0
                if col_count >= col_limit:
                    same_rows = [i for i, cl in enumerate(cols_set_len) if cl not in col_len]
                    for r in same_rows:
                        matrix[r][c] = matrix[r][c] + f'_{c}'
                break
    df = pd.DataFrame(matrix.T).rename(index={i: f'時段{i}' for i in range(time_num)}, columns={i: f for i, f in enumerate(foreign_list)}).replace(regex=r'.*_null_.*', value='')
    df.to_excel(f'{pwd}/schedule.xlsx')
    return df


def main():
    df = pd.read_excel(f'{pwd}/B2B媒合1122.xlsx').fillna('').query('`回覆` == ""')
    df = df[['單位名稱', '台灣公司名稱']]
    schedule(df)


if __name__ == '__main__':
    main()
