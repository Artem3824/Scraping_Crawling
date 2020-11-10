# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose

def int_price(value):
    return value.replace('\xa0','').replace('₽','')


class NikeItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    subtitle = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(int_price), output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())



