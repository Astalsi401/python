from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

URL = 'https://modernhousevn.com/collections/new-arrival/products/giuong-ngu-mh-21'
driver.get(URL)
sleep(3)
des = driver.find_elements(By.XPATH, "//strong[contains(text(),'Chất liệu :')]/../following-sibling::ul[1]/li")
print([d.text for d in des])
