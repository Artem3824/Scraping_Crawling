from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

main_link = 'https://www.nike.com/w/new-mens-jordan-black-lifestyle-13jrmz37eefz3n82yz90poyznik1'

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.get(main_link)

products_on_page = driver.find_element_by_class_name('wall-header__item_count').text
amount_of_products = products_on_page.split('(')[-1].split(')')[0]


while True:
    driver.implicitly_wait(2)
    product = driver.find_elements_by_class_name('product-card')[-1]
    product_position = product.get_attribute('data-product-position')
    action = ActionChains(driver)
    action.move_to_element(product)
    action.perform()

    if product_position == amount_of_products:
        break

products_list = driver.find_elements_by_class_name('product-card__body')

fieldnames = ['name', 'subtitle', 'price', 'URL']
with open('nike.csv', 'a', newline='', encoding='utf-8') as outfile_csv:
    writer = csv.DictWriter(outfile_csv, delimiter=',', fieldnames=fieldnames)
    writer.writeheader()
    for item in products_list:
        nike_dict = {}
        url_product = item.find_element_by_class_name('product-card__link-overlay').get_attribute('href')
        name_product = item.find_element_by_class_name('product-card__title').text
        subtitle_product = item.find_element_by_class_name('product-card__subtitle').text
        price_product = item.find_element_by_xpath(".//div[@data-test='product-price']").text

        nike_dict['name'] = name_product
        nike_dict['subtitle'] = subtitle_product
        nike_dict['price'] = price_product
        nike_dict['URL'] = url_product

        writer.writerow(nike_dict)



