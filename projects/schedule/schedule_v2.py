import pandas as pd
import numpy as np
from os.path import dirname, abspath
from random import sample

pwd = dirname(abspath(__file__)).replace('\\', '/')

row_m = {
    '': [],
    '': []
}


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
    total_count = 0
    total_limit = 1000
    while 1:
        col_count = 0
        col_limit = 50000
        total_count += 1
        #matrix = np.array([sameLen(sample(colname, row_m[colname], len(row_m[colname])), time_num) for colname in row_m])
        matrix = np.array([sample(foreign[foreign_list[0]], time_num)])
        status = False
        if total_count >= total_limit:
            break
        for c in range(1, foreign_num):
            if col_count >= col_limit:
                status = True
                break
            col_count = 0
            while 1:
                matrix_n = np.append(matrix, [sample(foreign[foreign_list[c]], time_num)], axis=0)
                cols = [matrix_n[:, col] for col in range(time_num)]
                cols_set = [set(col) for col in cols]
                col_count += 1
                col_len = [len(col) for col in cols]
                cols_set_len = [len(col) for col in cols_set]
                if col_len == cols_set_len:
                    matrix = matrix_n
                    print(f'total_count: {total_count} {foreign_list[c]} (col {c}) calc {col_count} times')
                    col_count = 0
                    break
                elif col_count >= col_limit:
                    print(f'重複! total_count: {total_count} {foreign_list[c]} (col {c}) calc {col_count} times')
                    break
        if status:
            continue
        else:
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
