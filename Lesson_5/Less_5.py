from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions as SE
from pymongo import MongoClient
import time
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['Mvideo']
products_db = db['products']

chrome_option = Options()
chrome_option.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_option)

driver.get('https://www.mvideo.ru/')

actions = ActionChains(driver)
actions.move_by_offset(100, 100).click().perform()
actions.move_to_element(driver.find_element_by_xpath('//h2[contains(text(),"Новинки")]/../../../div//li')).perform()

while True:
    wait = WebDriverWait(driver, 10)
    try:
        button_wait = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//h2[contains(text(),"Новинки")]/../../../div//a[contains(@class,"i-icon-fl-arrow-right")]')))
        button_wait.click()
        time.sleep(0.5)
    except SE.TimeoutException:
        break

item = driver.find_element_by_xpath('//h2[contains(text(),"Новинки")]/../../../../div/script')
prod_script = item.get_attribute('innerHTML')
prod_script = prod_script.replace('window.GTMMultiGalleryBlock = ', '').replace(
    ' window.GTMPush && window.GTMPush.updateDataPush(window.GTMMultiGalleryBlock); ', '')

products_db.delete_many({})
prod_list = eval(prod_script)
# products_db.insert_many(prod_list)

for i in prod_list:
    prod_list_res = {}
    prod_list_res['brand'] = i['eventProductBrand']
    prod_list_res['name'] = i['eventProductName']
    prod_list_res['price'] = float(i['eventProductSalePrice'])
    products_db.insert_one(prod_list_res)

for item in products_db.find():
    print(item)