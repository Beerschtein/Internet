# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def pr(price):
    try:
        price = int(price.replace(' ', ''))
    except Exception:
        price = price
    return price


class LeruaruItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(pr), output_processor=TakeFirst())
    metric_price = scrapy.Field(output_processor=TakeFirst())
    metric_price_2 = scrapy.Field(output_processor=TakeFirst())
    pictures = scrapy.Field()