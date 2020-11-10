# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
from itemadapter import ItemAdapter
from pymongo import MongoClient
from dictionary.spiders.medical import MedicalSpider


class DictionaryPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.medical_dictionary


    def process_item(self, item, spider):
        if len(item) == 3:
            item['definition'] = ''.join(item['definition']).strip().replace('\n', ' ')
            item['link'] = item['link'][0]
            if len(item['aword']) > 1:
                item['aword'] = ''.join(item['aword']).strip()
            else:
                item['aword'] = item['aword'][0]
        else:
            item['definition'] = 'not provided'
            item['link'] = item['link'][0]
            if len(item['aword']) > 1:
                item['aword'] = ''.join(item['aword']).strip()
            else:
                item['aword'] = item['aword'][0]

        collection = self.mongo_base[item['aword'][0].lower()]
        collection.insert_one(item)
        return item


class CSVPipeline(object):
    def __init__(self):
        self.file = f'dictionary.csv'
        with open(self.file, 'r', newline='') as csv_file:
            self.tmp_data = csv.DictReader(csv_file).fieldnames

        self.csv_file = open(self.file, 'a', newline='', encoding='utf-8')

    def process_item(self, item, spider):
        columns = item.fields.keys()

        data = csv.DictWriter(self.csv_file, columns)
        if not self.tmp_data:
            data.writeheader()
            self.tmp_data = True
        data.writerow(item)
        return item

    def __del__(self):
        self.csv_file.close()