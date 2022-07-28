from os.path import dirname, abspath
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

pwd = dirname(abspath(__file__)).replace('\\', '/')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

accounts_list = []
with open(f'{pwd}/test.txt', 'r') as f:
    accounts_list = [line.strip() for line in f]

res = []
for i in range(0, len(accounts_list), 2):
    res.append([accounts_list[i], accounts_list[i + 1]])

print(res)
