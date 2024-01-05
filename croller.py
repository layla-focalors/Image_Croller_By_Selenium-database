from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
import pymysql
from selenium.webdriver.common.alert import Alert
import time
import pymysql
import random
import os
conn = pymysql.connect(host='', user='', password='', db='imozi_datasets', charset='utf8')
cursor = conn.cursor() 

option = Options()
option.add_argument("disable-infobars")
option.add_argument("disable-extensions")
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"
option.add_argument('user-agent=' + user_agent)
option.add_argument('disable-gpu')
option.add_argument('incognito')
option.add_argument('headless')
s = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=s, options=option)

browser.get('https://e.kakao.com/item/new')
count = 0

imozi_name_base = []
imozi_link_base = []

SCROLL_PAUSE_SEC = 0.1
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_SEC)
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    
# #kakaoContent > div > ul > li:nth-child(1)
listai = browser.find_element(By.CSS_SELECTOR, '#kakaoContent > div > ul')
repeat = listai.find_elements(By.TAG_NAME, 'li')
for i in repeat:
    count += 1
for n in range(1, count - 2):
    cp = browser.find_element(By.CSS_SELECTOR, f'#kakaoContent > div > ul > li:nth-child({n})')
    imozi_name = cp.find_element(By.CSS_SELECTOR, 'div > a > div > strong > span').text
    imozi_url = cp.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    sql = f"INSERT INTO service (imozi_name, imozi_url) values (%s, %s)"
    # sql = f"INSERT INTO dev (imozi_count, imozi_name, imozi_url) values(NULL,'nul, 'mia')"

    print(imozi_name)
    cursor.execute(sql, (imozi_name, imozi_url))
    # cursor.execute("show tables")
    print({"imozi_name": imozi_name, "imozi_url": imozi_url})
    conn.commit()
conn.close()
