from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
import json
import hashlib
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time

def db_create():
    client = MongoClient('127.0.0.1', 27017)
    mongo_db = client['data_mail']

    try:
        collection = mongo_db.create_collection('mail')
    except BaseException:
        collection = mongo_db.email

    return collection


driver = webdriver.Chrome(executable_path='./chromedriver.exe')

driver.get('https://mail.ru')

login = driver.find_element_by_name('login')
login.send_keys('study.ai_172')
login.send_keys(Keys.ENTER)
time.sleep(2)

passw = driver.find_element_by_name('password')
passw.send_keys('NextPassword172???')
time.sleep(5)
passw.send_keys(Keys.ENTER)
time.sleep(10)

for i in range(2):
    time.sleep(5)
    container = driver.find_elements_by_css_selector("div.llc__container")
    actions = ActionChains(driver)
    actions.move_to_element(container[-1])
    actions.perform()

all_mail = []
email = driver.find_elements_by_class_name('llc__content')
for mail in email:
    data_mail = {}
    data_mail['sender'] = mail.find_element_by_class_name("ll-crpt").get_attribute("title")
    data_mail['title'] = mail.find_element_by_class_name("ll-sj__normal").text
    data_mail['body'] = mail.find_element_by_class_name('ll-sp__normal').text
    all_mail.append(data_mail)
    email_binary = json.dumps(data_mail).encode('utf-8')
    mail_hash = hashlib.sha3_256(email_binary)
    mail_id = mail_hash.hexdigest()
    data_mail['_id'] = mail_id

    try:
        collection.insert_one(data_mail)
    except BaseException:
        continue

driver.close()
