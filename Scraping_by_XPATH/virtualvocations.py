import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient
from bs4 import BeautifulSoup

'''Connection to DataBase'''
client = MongoClient('localhost', 27017)
db = client['foreign_jobs']
jobs_db = db.jobs


main_link = 'https://www.virtualvocations.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

search_title = input('Enter a title: ')

def virtualvocations(search):
    response = requests.get(f'{main_link}/jobs/q-{search}/c-100%25+remote', headers=headers)

    while True:
        root = html.fromstring(response.text)
        jobs_cards = root.xpath("//li[@class='card-item job-card']")

        for job in jobs_cards:
            job_dict = {}
            job_title = job.xpath(".//a")[0].xpath("string()")
            job_url = job.xpath(".//a/@href")[0]
            job_description_data = job.xpath(".//p")[0].xpath("string()")
            job_description = ''.join(job_description_data).replace('\n', '').replace('\t', '').strip()
            job_data = job.xpath(".//span[@class='meta']/text()")[0]

            job_dict['source'] = main_link
            job_dict['title'] = job_title
            job_dict['date'] = job_data
            job_dict['URL'] = job_url
            job_dict['description'] = job_description

            jobs_db.update_one({'URL': job_dict['URL']}, {'$set': job_dict}, upsert=True)

        '''Pagination'''
        next_page_url = root.xpath("//ul[@class='pagination']//a[@rel='next']/@href")
        if next_page_url:
            next_page = next_page_url[0]
        else:
            break
        response = requests.get(next_page, headers=headers)

virtualvocations(search_title)
