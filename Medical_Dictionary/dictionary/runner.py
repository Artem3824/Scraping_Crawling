from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from dictionary import settings
from dictionary.spiders.medical import MedicalSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process_object = CrawlerProcess(settings=crawler_settings)

    process_object.crawl(MedicalSpider, letter='a')
    process_object.crawl(MedicalSpider, letter='b')
    process_object.crawl(MedicalSpider, letter='c')
    process_object.crawl(MedicalSpider, letter='d')
    process_object.crawl(MedicalSpider, letter='e')
    process_object.crawl(MedicalSpider, letter='f')
    process_object.crawl(MedicalSpider, letter='g')
    process_object.crawl(MedicalSpider, letter='h')
    process_object.crawl(MedicalSpider, letter='i')
    process_object.crawl(MedicalSpider, letter='j')
    process_object.crawl(MedicalSpider, letter='k')
    process_object.crawl(MedicalSpider, letter='l')
    process_object.crawl(MedicalSpider, letter='m')
    process_object.crawl(MedicalSpider, letter='n')
    process_object.crawl(MedicalSpider, letter='o')
    process_object.crawl(MedicalSpider, letter='p')
    process_object.crawl(MedicalSpider, letter='q')
    process_object.crawl(MedicalSpider, letter='r')
    process_object.crawl(MedicalSpider, letter='s')
    process_object.crawl(MedicalSpider, letter='t')
    process_object.crawl(MedicalSpider, letter='u')
    process_object.crawl(MedicalSpider, letter='v')
    process_object.crawl(MedicalSpider, letter='w')
    process_object.crawl(MedicalSpider, letter='x')
    process_object.crawl(MedicalSpider, letter='y')
    process_object.crawl(MedicalSpider, letter='z')
    process_object.start()
