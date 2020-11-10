# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst

# def clear_definition(value):
#     if value:
#         value = ''.join(value).strip()
#     else:
#         value = None
#     return value

class DictionaryItem(scrapy.Item):
    _id = scrapy.Field()
    aword = scrapy.Field()
    definition = scrapy.Field()
    link = scrapy.Field()
