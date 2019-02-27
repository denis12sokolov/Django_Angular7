import json
import logging
import re
import sys
import time
from itertools import chain

from selenium.common.exceptions import NoSuchElementException

from core.parser.helpers import make_soup, get_type_by_name

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

PRICE = re.compile(r"(\$)|(\xa0)|(\s)|(CAD)|(RUB)|(,)")


def get_price_from_attr(attr_data):
    data = json.loads(attr_data)
    return float(data["original"][0].replace("$", ""))


def get_main_price(product):
    element = product.find("span", class_="list_price")
    if element:
        price = PRICE.sub('', element.text).replace(",", ".")
        price = price.split("-")[0]
        return price if price[0].isdigit() else price[1:]
    else:
        return 0


def get_discount_price(product):
    element = product.find("span", class_="current_price")
    if element:
        price = PRICE.sub('', element.text).replace(",", ".")
        price = price.split("-")[0]
        return price if price[0].isdigit() else price[1:]
    else:
        return 0


def get_product_name(product):
    element = product.find("a", class_="item-name")
    if element:
        return element.get_text()


def get_image_url(product):
    img_element = product.find("img", "product-listing-image")
    if img_element:
        return img_element.attrs['src']


def get_original_url(product):
    element = product.find("a", class_="item-name")
    if element:
        return element.attrs["href"]


def parse_product(product):
    try:
        product_name = get_product_name(product)
        parsed_product = {
            "list_price": get_main_price(product),
            "discount_price": get_discount_price(product),
            "name": product_name,
            "url_img": get_image_url(product),
            "product_type": get_type_by_name(product_name),
            "url_original": get_original_url(product),
        }
        return parsed_product
    except:
        logging.info("Item Champion is skipped")


def parse_next_page(driver, sources):
    try:
        driver.execute_script("window.scrollTo(0, 20000)")
        driver.implicitly_wait(15)
        time.sleep(5)
        sources.append(driver.page_source)
        next_button = driver.find_element_by_class_name("paging-arrow-right")
        if 'invisible' not in next_button.get_attribute("class"):
            driver.execute_script("arguments[0].click();", next_button)
            parse_next_page(driver, sources)
    except NoSuchElementException:
        pass


def parse_source(source):
    return make_soup(source).find_all("div", class_="each-product")


def parse_champion_page(driver, url):
    driver.get(url)
    driver.implicitly_wait(15)
    time.sleep(5)
    sources = []
    parse_next_page(driver, sources)
    product_list = chain.from_iterable(map(parse_source, sources))
    return filter(bool, map(parse_product, product_list))
