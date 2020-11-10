# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Compose

def int_price(price_value):
    return int(price_value.replace(' ', ''))

def clean_definition(product_specifications):
    product_specifications = product_specifications.strip().replace(' ', '').replace('\n', '')
    return product_specifications

class LeroymerlinItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(int_price), output_processor=TakeFirst())
    photo = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    item_keys = scrapy.Field()
    item_values = scrapy.Field(input_processor=MapCompose(clean_definition))
    item_specification = scrapy.Field()
