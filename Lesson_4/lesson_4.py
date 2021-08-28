from lxml import html
from pprint import pprint
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
          'Accept': '*/*'}

response = requests.get('https://lenta.ru/')
dom = html.fromstring(response.text)
lenta_News = []
all_news = []

items = dom.xpath("//div[@class = 'span4']/div[@class = 'item' or @class = 'first-item']")
for item in items:
    news = {}
    news['time'] = item.xpath(".//time[@class = 'g-time']/text()")
    news['date'] = item.xpath(".//time/@title")
    news_l = item.xpath(".//a/@href")
    news['link'] = f'https://lenta.ru{news_l[0]}'
    news['news'] = item.xpath(".//a[contains (@href, '/news/')]/text()")
    news['resource'] = "lenta.ru"
    all_news.append(news)

    # В нашем словаре обнаружены пропуски \\xa0" и также мы скачали (, 'Отменить')
    # Переведём словарь в строку
    strings = []
    for key, item in news.items():
        strings.append("{}: {}".format(key.capitalize(), item))
    result = "; ".join(strings)
    new_result = result.replace(u"\\xa0", u" ").replace(u", 'Отменить'", u"")
    lenta_News.append(new_result)
# Обработав данные мы видим дубли новостей, уберём лишнее
all_lenta_News = []
for x in lenta_News:
    if x not in all_lenta_News:
        all_lenta_News.append(x)

# Выведем все новости сайта
pprint(all_lenta_News)