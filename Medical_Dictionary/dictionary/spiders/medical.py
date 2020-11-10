import scrapy
from scrapy.http import HtmlResponse
from dictionary.items import DictionaryItem
from scrapy.loader import ItemLoader


class MedicalSpider(scrapy.Spider):
    name = 'medical'
    allowed_domains = ['merriam-webster.com']

    def __init__(self, letter):
        self.start_urls = [f'https://www.merriam-webster.com/browse/medical/{letter}']

    def parse(self, response:HtmlResponse):
        links_to_definition = response.xpath("//div[@class='entries']/ul/li/a/@href").extract()
        for link in links_to_definition:
            yield response.follow(link, callback=self.parse_definition)

        next_page = response.xpath("//li[@class='next']/a/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_definition(self, response:HtmlResponse):
        loader = ItemLoader(item=DictionaryItem(), response=response)
        loader.add_xpath('aword', "//h1/text() | //h1/span/text()")
        loader.add_xpath('definition', "//div[@id='medical-entry-1']/div[@class='vg']//span[@class='dtText']/em[@class='mw_t_it']/text() | //div[@id='medical-entry-1']/div[@class='vg']//span[@class='dtText']/text()")
        loader.add_value('link', response.url)
        yield loader.load_item()