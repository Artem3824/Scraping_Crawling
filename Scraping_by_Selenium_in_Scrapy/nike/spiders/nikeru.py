import scrapy
from scrapy.http import HtmlResponse
from nike.items import NikeItem
from scrapy.loader import ItemLoader
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


class NikeruSpider(scrapy.Spider):
    name = 'nikeru'
    allowed_domains = ['nike.com']
    start_urls = ['https://www.nike.com/ru/w/new-mens-nike-lifestyle-shoes-13jrmz3n82yz7yfbznik1zy7ok']

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response: HtmlResponse):
        self.driver.get(response.url)

        products_on_page = self.driver.find_element_by_class_name('wall-header__item_count').text
        amount_of_products = products_on_page.split('(')[-1].split(')')[0]

        while True:
            self.driver.implicitly_wait(2)
            product = self.driver.find_elements_by_class_name('product-card')[-1]
            product_position = product.get_attribute('data-product-position')
            action = ActionChains(self.driver)
            action.move_to_element(product)
            action.perform()

            if product_position == amount_of_products:
                products_list = self.driver.find_elements_by_class_name('product-card__link-overlay')
                for link in products_list:
                    product_link = link.get_attribute('href')
                    yield response.follow(product_link, callback=self.product_parse)
                break


    def product_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=NikeItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('subtitle', "//h2/text()")
        loader.add_xpath('price', "//div[@data-test='product-price']/text()")
        loader.add_value('link', response.url)
        yield loader.load_item()
