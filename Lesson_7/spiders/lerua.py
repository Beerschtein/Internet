import scrapy
from leruaru.items import LeruaruItem
from scrapy.loader import ItemLoader


class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']

    # start_urls = ['http://leroymerlin.ru/']

    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response):
        links = response.xpath("//a[@data-qa='product-image']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_in)

        next = response.xpath("//a[contains(@aria-label, 'Следующая страница:')]/@href").get()
        if next:
            yield response.follow(next, callback=self.parse)

    def parse_in(self, response):
        loader = ItemLoader(item=LeruaruItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', "//uc-pdp-price-view[@slot='primary-price']/span[@slot='price']/text()")
        loader.add_xpath('metric_price', "//uc-pdp-price-view[@slot='primary-price']/span[@slot='currency']/text()")
        loader.add_xpath('metric_price_2', "//uc-pdp-price-view[@slot='primary-price']/span[@slot='unit']/text()")
        loader.add_xpath('pictures', '//picture[@slot="pictures"]/source[1]/@data-origin')
        loader.add_value('url', response.url)
        yield loader.load_item()

        # url = response.url
        # name = response.xpath('//h1/text()').get()
        # price = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span[@slot='price']/text()").get()
        # metric_price = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span[@slot='currency']/text()").get()
        # metric_price_2 = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span[@slot='unit']/text()").get()
        # pictures = response.xpath('//picture[@slot="pictures"]/source[1]/@data-origin').getall()
        # yield LeruaruItem(url=url, name=name, price=price, metric_price=metric_price, metric_price_2=metric_price_2, pictures=pictures)