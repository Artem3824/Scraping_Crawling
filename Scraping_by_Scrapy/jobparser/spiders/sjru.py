import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']

    def __init__(self, job_vac):
        self.start_urls = [f'https://www.superjob.ru/vacancy/search/?keywords={job_vac}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()

        if next_page:
            page_number = next_page[-2:]
            yield response.follow(next_page, callback=self.parse)
        else:
            page_number = 'The end'

        vacancy_links = response.xpath("//div[@class='_3mfro PlM3e _2JVkc _3LJqf']/a/@href").extract()
        print(self.allowed_domains[0], f'*** Page number {page_number}, links per page: ', len(vacancy_links))

        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name1 = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract_first()
        salary1 = response.xpath("//span[@class='_3mfro _2Wp8I PlM3e _2JVkc']/text()").extract()
        url1 = response.url
        source = self.allowed_domains[0]
        yield JobparserItem(name=name1, salary=salary1, url=url1, source=source)
