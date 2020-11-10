import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self, job_vac):
        self.start_urls = [
            f'https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text={job_vac}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()

        if next_page:
            page_number = next_page[-2:]
            yield response.follow(next_page, callback=self.parse)
        else:
            page_number = 'The end'


        vacancy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        print(self.allowed_domains[0], f'*** Page number {page_number}, links per page: ', len(vacancy_links))

        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name1 = response.xpath("//h1[@class='bloko-header-1']/text()").extract_first()
        salary1 = response.xpath("//p[@class='vacancy-salary']/span[@data-qa='bloko-header-2']/text()").extract()
        url1 = response.url
        source = self.allowed_domains[0]
        yield JobparserItem(name=name1, salary=salary1, url=url1, source=source)
