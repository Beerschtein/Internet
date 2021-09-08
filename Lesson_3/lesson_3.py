from bs4 import BeautifulSoup as bs
from pprint import pprint
from pymongo import MongoClient
import re
import requests

class ParsingJob:

    def __init__(self, ip, port, db_name, collection_name):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Accept': '*/*'}

        self.link_hh = 'https://hh.ru/search/vacancy'

        self.mongodb = MongoClient(ip, port)
        self.db = self.mongodb[db_name]
        self.collection = self.db[collection_name]

    def print_salary_max_gt(self, salary):
        objects = self.collection.find({'salary_max': {'$gt': salary}})
        for obj in objects:
            pprint(obj)

    def print_salary_min_gt(self, salary):
        objects = self.collection.find({'salary_min': {'$gt': salary}})
        for obj in objects:
            pprint(obj)

    def search_job(self, vacancy):
        self.parser_hh(vacancy)

    def is_exists(self, name_tags, field):
        return bool(self.collection.find_one({name_tags: {"$in": [field]}}))

    def parser_hh(self, vacancy):
        params = {
            'text': vacancy,
            'page': ''
        }

        html = requests.get(self.link_hh, params=params, headers=self.headers)

        if html.ok:
            parsed_html = bs(html.text, 'html.parser')

            page_block = parsed_html.find('div', {'data-qa': 'pager-block'})
            if not page_block:
                last_page = 1
            else:
                last_page = page_block.find_all('a', {'class': 'bloko-button'})
                last_page = int(last_page[len(last_page) - 2].find('span').getText())

        for page in range(0, last_page):
            params['page'] = page
            html = requests.get(self.link_hh, params=params, headers=self.headers)

            if html.ok:
                parsed_html = bs(html.text, 'html.parser')

                vacancy_items = parsed_html.find_all('div', {'class': 'vacancy-serp-item'})
                for item in vacancy_items:
                    vacancy = self.parser_item_hh(item)
                    if self.is_exists('vacancy_link', vacancy['vacancy_link']):
                        self.collection.update_one({'vacancy_link': vacancy['vacancy_link']}, {'$set': vacancy})
                    else:
                        self.collection.insert_one(vacancy)

    def parser_item_hh(self, item):

        vacancy_data = {}

        vacancy_name = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}) \
            .getText().replace(u'\xa0', u' ')

        vacancy_data['vacancy_name'] = vacancy_name

        company_name = item.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})

        if company_name:
            company_name = company_name.getText().replace(u'\xa0', u' ')
        vacancy_data['company_name'] = company_name

        city = item.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}) \
            .getText() \
            .split(', ')[0]

        vacancy_data['city'] = city
        salary = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not salary:
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
            salary = salary.getText().replace(u'\u202f', u'')
            salary = salary.replace('–', '')
            salary = re.split(r'\s', salary)

            if salary[0] == 'до':
                salary_min = None
                salary_max = int(salary[1])
            elif salary[0] == 'от':
                salary_min = int(salary[1])
                salary_max = None
            else:
                salary_min = int(salary[0])
                salary_max = int(salary[2])

            salary_currency = salary[len(salary) - 1]

        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['salary_currency'] = salary_currency

        vacancy_link = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']

        vacancy_data['vacancy_link'] = vacancy_link
        vacancy_data['site'] = 'hh.ru'

        return vacancy_data

vacancy_db = ParsingJob('127.0.0.1', 27017, 'vacancy',
                        'vacancy_db')

vacancy = 'Python'
vacancy_db.search_job(vacancy)
objects = vacancy_db.collection.find().limit(2)
for obj in objects:
    pprint(obj)

print(' Ниже зарплаты \n')
vacancy_db.print_salary_max_gt(150000)  # Максимальная зп
# vacancy_db.print_salary_min_gt(300000) - минимальная ЗП