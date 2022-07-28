from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep


'''
/../following-sibling::ul[1]/li
'''
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
try:
    driver.get('https://modernhousevn.com/collections/new-arrival/products/bo-ban-an-anna-tu-nhien-4-ghe')
except Exception:
    pass
sleep(5)
target = driver.find_element(By.XPATH, "//strong[contains(text(),'Chất liệu')]/..")
while target.tag_name != 'p' and target.find_element(By.XPATH, "./..").get_attribute("class") != 'panel-body':
    target = target.find_element(By.XPATH, "./..")
des = target.find_elements(By.XPATH, './following-sibling::ul[1]/li')
print([d.text for d in des])
