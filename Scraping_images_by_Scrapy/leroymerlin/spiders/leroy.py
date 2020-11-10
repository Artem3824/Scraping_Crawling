import scrapy
from scrapy.http import HtmlResponse
from leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, category):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={category}']

    def parse(self, response: HtmlResponse):
        items_list = response.xpath("//a[@slot='picture']/@href").extract()
        for link in items_list:
            yield response.follow(link, callback=self.item_parse)

        next_page = response.xpath("//div[@class='next-paginator-button-wrapper']/a/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def item_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photo', "//picture[@slot='pictures']/source/@srcset")
        loader.add_xpath('item_keys', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('item_values', "//dd[@class='def-list__definition']/text()")
        yield loader.load_item()
