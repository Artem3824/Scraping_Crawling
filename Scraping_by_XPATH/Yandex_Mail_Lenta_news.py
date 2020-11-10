import requests
from pprint import pprint
from lxml import html
from datetime import datetime
import re
from pymongo import MongoClient

'''Connection to DataBase'''
client = MongoClient('localhost', 27017)
db = client['top_news']
yandex = db.yandex_news
lenta = db.lenta_news
mail = db.mail_news

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
mail_link = 'https://news.mail.ru/'
lenta_link = 'https://lenta.ru'
yandex_link = 'https://yandex.ru/news/'

'''Get news from Yandex - https://yandex.ru/news/'''
def yandex_news():
    response = requests.get(yandex_link, headers=headers)
    root = html.fromstring(response.text)
    articles = root.xpath("//article[contains(@class, 'mg-card news-card')]")

    for article in articles:
        yandex_dict = {}
        yandex_dict['name'] = article.xpath(".//h2[@class='news-card__title']/text()")[0].strip().replace('\n', '')
        yandex_dict['url'] = article.xpath(".//a[@class='news-card__link']/@href")[0]
        yandex_dict['source'] = article.xpath(".//span[@class='mg-card-source__source']/a/text()")[0]
        yandex_dict['time'] = article.xpath(".//span[@class='mg-card-source__time']/text()")[0]

        '''Import scraped news into DataBase'''
        yandex.update_one({'url': yandex_dict['url']}, {'$set': yandex_dict}, upsert=True)

'''Get news from Lenta - https://lenta.ru'''
def lenta_news():
    response = requests.get(lenta_link, headers=headers)
    root = html.fromstring(response.text)
    topic_news = root.xpath("//div[@class='span4']/section/div[@class='item news b-tabloid__topic_news']")
    for news in topic_news:
        lenta_dict = {}
        lenta_dict['name'] = news.xpath(".//div[@class='titles']/h3/a/span/text()")[0].replace('\xa0', ' ')
        lenta_url = news.xpath(".//div[@class='titles']/h3/a/@href")[0]
        if 'http' in lenta_url:
            lenta_dict['url'] = lenta_url
            source_pattern = re.compile('\/{2}(\w+.\w+)\/')
            lenta_dict['source'] = 'https://' + re.findall(source_pattern, lenta_url)[0]
        else:
            lenta_dict['url'] = lenta_link + lenta_url
            lenta_dict['source'] = lenta_link
        lenta_dict['time'] = news.xpath(".//span[@class='g-date item__date']/span[@class='time']/text()")[0]

        '''Import scraped news into DataBase'''
        lenta.update_one({'url': lenta_dict['url']}, {'$set': lenta_dict}, upsert=True)


def get_time_and_source(url):
    get_info = requests.get(url, headers=headers)
    root_page = html.fromstring(get_info.text)
    posted_time = root_page.xpath("//span[@class='note']/span[@datetime]")[0].items()
    data_time = posted_time[1][1]
    convert_time = datetime.strptime(data_time, r'%Y-%m-%dT%H:%M:%S%z')
    result_time = convert_time.strftime('%H:%M')
    source = root_page.xpath("//span[@class='breadcrumbs__item']//span[@class='link__text']/text()")[0]
    return result_time, source

def picture_news(list_of_objects):
    start_list = []
    for news in list_of_objects:
        start_dict = {}
        start_dict['name'] = news.xpath(".//span[contains(@class,'photo__title')]/text()")[0].replace('\xa0', ' ')
        start_dict['url'] = news.xpath(".//@href")[0]
        time_and_source = get_time_and_source(start_dict['url'])
        start_dict['time'] = time_and_source[0]
        start_dict['source'] = time_and_source[1]
        start_list.append(start_dict)
    return start_list

def top6_news(list_of_objects):
    top6_news_list = []
    for news in list_of_objects:
        main_dict = {}
        main_dict['url'] = news.xpath(".//a/@href")[0]
        main_dict['name'] = news.xpath(".//a/text()")[0].replace('\xa0', ' ')
        time_and_source = get_time_and_source(main_dict['url'])
        main_dict['time'] = time_and_source[0]
        main_dict['source'] = time_and_source[1]
        top6_news_list.append(main_dict)
    return top6_news_list

'''Get top6 news and news from pictures from Mail - https://news.mail.ru/'''
def mail_news():
    response = requests.get(mail_link, headers=headers)
    root = html.fromstring(response.text)
    mail_news_list = []
    start_news = root.xpath("//a[contains(@class,'js-topnews__item')]")
    main_news = root.xpath("//li[@class='list__item']")[:6]
    mail_news_list.append(picture_news(start_news))
    mail_news_list.append(top6_news(main_news))
    mail_news_list = [i for list in mail_news_list for i in list]

    '''Import scraped news into DataBase'''
    for i in mail_news_list:
        mail.update_one({'url': i['url']}, {'$set': i}, upsert=True)


mail_news()
yandex_news()
lenta_news()




