import pandas as pd


# delete if df['value1'] == 0
condition1 = [{'col': ['value1'], 'val': [0]}]
# delete if df['value1'] == 0 & df['value2'] == 0
condition2 = [{'value1': 0, 'value2': 0}]

df = pd.DataFrame(data=[['A', 2, 0],
                        ['B', 5, 1],
                        ['C', 0, 1],
                        ['X', 0, 1],
                        ['X', 0, 0]],
                  columns=['name', 'value1', 'value2'])

cond = pd.DataFrame(condition2)
out = df.merge(cond, how='left', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])


print(out)
