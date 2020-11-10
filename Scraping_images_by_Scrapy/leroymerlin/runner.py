from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from leroymerlin import settings
from leroymerlin.spiders.leroy import LeroySpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process_object = CrawlerProcess(settings=crawler_settings)
    process_object.crawl(LeroySpider, category='молоток')
    process_object.start()
