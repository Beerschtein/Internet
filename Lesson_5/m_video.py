from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions

MONGO_URI = 'mongodb://172.17.0.2:27017/'
MONGO_DATABASE = 'mvideo_db'

client = MongoClient(MONGO_URI)
mongo_base = client[MONGO_DATABASE]
collection = mongo_base['hits']

driver = webdriver.Chrome(executable_path='./chromedriver.exe')

driver.get('https://www.mvideo.ru')

title_site = 'М.Видео'

assert title_site in driver.title

hits = driver.find_element_by_xpath('//div[@class="fl-product-tile c-product-tile fl-product-tile_gallery-product-set"]')

while True:
    try:
        next_button = WebDriverWait(hits, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[class="next-btn sel-hits-button-next"]')
            )
        )

        driver.execute_script("$(arguments[0]).click();", next_button)
    except exceptions.TimeoutException:
        print('Сбор данных окончен')
        break

goods = hits.find_elements_by_css_selector('li.gallery-list-item')

item = {}
for good in goods:
    item['title'] = good.find_element_by_css_selector(
        'a.sel-product-tile-title') \
        .get_attribute('innerHTML')

    item['good_link'] = good.find_element_by_css_selector(
        'a.sel-product-tile-title') \
        .get_attribute('href')

    item['price'] = float(
        good.find_element_by_css_selector(
            'div.c-pdp-price__current').get_attribute('innerHTML').replace(
                '&nbsp;', '').replace('¤', ''))

    item['image_link'] = good.find_element_by_css_selector(
        'img[class="lazy product-tile-picture__image"]') \
        .get_attribute('src')

    collection.update_one({'good_link': item['good_link']}, {'$set': item},
                          upsert=True)
driver.quit()