# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import os
from urllib.parse import urlparse
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class LeroymerlinPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['item_specification'] = dict(zip(item['item_keys'], item['item_values']))
        item.pop('item_keys')
        item.pop('item_values')
        collection.insert_one(item)
        return item



class LeroymerlinPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        return f'files/{os.path.basename(urlparse(request.url).path)[:8]}/' + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        if results[0]:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        return item