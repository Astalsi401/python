import pandas as pd
import numpy as np
from timeit import timeit


df = pd.read_csv('D:/Documents/google/csv/生策會/2021-01-01_2021-12-31/source.csv')
n = 1000


def fuc0():
    return df[df['ga:source'].str.match(r"EZMail|line|edm|BenchmarkEmail|newsletter", na=False)]


def fuc1():
    df.query('`ga:source`.str.match("EZMail", na=False)')


def fuc2():
    df.query('`ga:source`=="EZMail"')


def fuc3():
    return df[df['ga:source'].isin(['EZMail', 'line', 'edm', 'BenchmarkEmail', 'newsletter'])]


def test(fuc, n):
    return round(timeit(fuc, number=n) / n, 5)


print(type({'ga:source': 'total'}))
print(fuc3())
print([test(fuc, n) for fuc in [fuc0, fuc3]])
