import pandas as pd
from os.path import dirname, abspath

pwd = dirname(abspath(__file__)).replace('\\', '/')

pd.read_csv(f'{pwd}/退件地址更新.csv').to_excel(f'{pwd}/退件地址更新.xlsx', index=False)
