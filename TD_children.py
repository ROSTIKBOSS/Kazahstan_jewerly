from selenium import webdriver
import time
import re
import pandas as pd
from auth_data import tdserebro_login, tdserebro_password
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(executable_path='chromedriver_1.exe')
driver.get('https://tdserebro.ru/astana/search?filter[nomGroups][]=57&sort=new:desc#filters')
time.sleep(5)
'''element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.locale_switcher li a"))
        )
language = driver.find_element_by_css_selector('div.locale_switcher li a').click()'''

print('to be sure')
element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.website-link"))
        )
city = driver.find_elements_by_css_selector('a.website-link')[0].click()
element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-launch.btn-sm"))
        )
enter = driver.find_elements_by_css_selector('a.btn.btn-launch.btn-sm')[0].click()
time.sleep(3)
username = driver.find_elements_by_css_selector("div.tab-content input#username")[0]
password = driver.find_elements_by_css_selector("div.tab-content input#password")[0]
username.send_keys('7771701044')
password.send_keys(tdserebro_password)
time.sleep(3)
logIn = driver.find_elements_by_css_selector("div.tab-content button#login_btn")[0].click()
time.sleep(3)
flag = 0
links = []
while flag == 0:
    l = driver.find_elements_by_css_selector('div.product_img_content > a')
    try:
        for item in l:
            links.append(item.get_attribute('href'))
        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-launch.loadMore"))
        )
        loadMore = driver.find_elements_by_css_selector('button.btn.btn-launch.loadMore')[0].click()
    except:
        flag = 1

# print(links)
print(len(set(links)))
df = pd.DataFrame(list(set(links)))
df.to_excel('TD_children_links.xls', index=False)
driver.close()
