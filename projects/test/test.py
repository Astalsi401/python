from os.path import dirname, abspath
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import undetected_chromedriver as uc
import threading

pwd = dirname(abspath(__file__)).replace('\\', '/')

# webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# uc.Chrome(use_subprocess=True)


def instance(n):
    return [webdriver.Chrome(service=Service(ChromeDriverManager().install())) for m in range(0, n)]


def Main(i):
    i.get('chrome://version/')


threads = [threading.Thread(target=Main, args=(i,)) for i in instance(int(input('Buy number : ')))]
for t in threads:
    t.start()
