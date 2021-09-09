from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from leruaru import settings
from leruaru.spiders.lerua import LeruaSpider



if __name__ == '__main__':
    crauler_settings = Settings()
    crauler_settings.setmodule(settings)
    search = 'ламинат'
    process = CrawlerProcess(crauler_settings)
    process.crawl(LeruaSpider, search=search)


    process.start()