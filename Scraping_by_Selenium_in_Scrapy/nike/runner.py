from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from nike import settings
from nike.spiders.nikeru import NikeruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process_object = CrawlerProcess(settings=crawler_settings)
    process_object.crawl(NikeruSpider)
    process_object.start()
