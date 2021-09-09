# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class LeruaruPipeline:
    def __init__(self):
        bd = MongoClient('localhost', 27017)
        self.base = bd.leruamerlen
    def process_item(self, item, spider):
        # item['price'] = float(item['price'].replace(' ', ''))
        item['metric_price'] = item['metric_price'] + '/' + item['metric_price_2']
        item.pop('metric_price_2')
        col = self.base[spider.name]
        ITEM = dict(item)
        if len([i for i in col.find(ITEM)]) == 0:
            col.insert_one(ITEM)
        return item



class leruaphotospipline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['pictures']:
            for img in item['pictures']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['pictures'] = [itm[1] for itm in results if itm[0] == True]
        return item