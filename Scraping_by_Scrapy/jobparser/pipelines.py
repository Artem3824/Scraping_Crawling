# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.russian_jobs_scrapy
        self.compensation = JobparserItemCompensationPipeline()

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item = self.compensation.item_adjustments(item, spider)
        collection.insert_one(item)
        return item

class JobparserItemCompensationPipeline(object):
    def item_adjustments(self, item, spider):
        item['min_salary'] = 0
        item['max_salary'] = 0
        item['currency'] = 0
        if spider.name == 'sjru':
            item = self.sjru_item_compensation(item)
        elif spider.name == 'hhru':
            item = self.hhru_item_compensation(item)
        return item

    def sjru_item_compensation(self, item):
        if len(item['salary']) >= 2:
            if item['salary'][0] == "от":
                item['min_salary'] = int(item['salary'][2][:-4].replace('\xa0', '').replace(' ', ''))
                item['currency'] = item['salary'][2][-4:]
            elif item['salary'][0] == "до":
                item['max_salary'] = int(item['salary'][2][:-4].replace('\xa0', '').replace(' ', ''))
                item['currency'] = item['salary'][2][-4:]
            elif item['salary'][0].replace('\xa0', '').replace(' ', '').isnumeric() and len(item['salary']) == 4:
                item['min_salary'] = int(item['salary'][0].replace('\xa0', '').replace(' ', ''))
                item['max_salary'] = int(item['salary'][1].replace('\xa0', '').replace(' ', ''))
                item['currency'] = item['salary'][-1]
            else:
                item['min_salary'] = int(item['salary'][0].replace('\xa0', '').replace(' ', ''))
                item['max_salary'] = int(item['salary'][0].replace('\xa0', '').replace(' ', ''))
                item['currency'] = item['salary'][-1]
        item['salary'] = ' '.join(item['salary']).replace('\xa0', '')
        return item


    def hhru_item_compensation(self, item):
        if len(item['salary']) != 0:
            for i in range(len(item['salary'])):
                if item['salary'][i] == "от ":
                    item['min_salary'] = int(item['salary'][i + 1].replace('\xa0', '').replace(' ', ''))
                elif (item['salary'][i] == " до ") | (item['salary'][i] == "до "):
                    item['max_salary'] = int(item['salary'][i + 1].replace('\xa0', '').replace(' ', ''))
                elif (item['salary'][i] == "руб.") | (item['salary'][i] == "USD") | (item['salary'][i] == "EUR"):
                    item['currency'] = item['salary'][i]
        item['salary'] = ''.join(item['salary']).replace('\xa0', '')
        return item
