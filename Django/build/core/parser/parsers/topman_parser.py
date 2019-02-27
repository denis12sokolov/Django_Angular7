import re
import time
from itertools import chain

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver

from core.parser.helpers import make_soup, get_type_by_name, is_bottom

ATTR_NAME = "data-auto-id"
PRICE = re.compile(r"(£)|(\xa0)|(RRP)|(Was)|(Now)|(\s)")

num_elements = set()


def get_main_price(product):
    element = product.find("span", class_="was1")
    if element:
        return PRICE.sub('', element.get_text())


def get_discount_price(product):
    element = product.find("span", class_="now")
    if element:
        return PRICE.sub('', element.get_text())


def get_product_name(product):
    element = product.find("a", class_="product_name")
    if element:
        return element.get_text().strip()


def get_image_url(product):
    img_element = product.find("img", class_="product_image")
    if img_element:
        return img_element.attrs['src']


def get_product_num(product):
    element = product.find("img", class_="product_image")
    if element:
        return element.attrs["data-partnumber"]


def get_original_url(product):
    element = product.find("a", class_="product_name")
    if element:
        return element.attrs["href"]


def parse_product(product):
    num_product = get_product_num(product)
    if num_product and num_product not in num_elements:
        price = get_main_price(product)
        dis_price = get_discount_price(product)
        num_elements.add(num_product)
        product_name = get_product_name(product)
        parsed_product = {
            "list_price": price if price else dis_price,
            "discount_price": dis_price if price else 0.0,
            "name": product_name,
            "url_img": get_image_url(product),
            "product_type": get_type_by_name(product_name),
            "url_original": "http://www.topman.com" + get_original_url(product),
        }
        return parsed_product


def set_grid_to_4(driver):
    try:
        driver.execute_script("document.getElementsByClassName('grid_4')[0].click()")
    except:
        pass


def parse_topman_page(driver: WebDriver, url):
    driver.get(url)
    driver.implicitly_wait(15)
    time.sleep(5)
    set_grid_to_4(driver)
    sources = [driver.page_source]
    position = 700
    while not is_bottom(driver):
        driver.execute_script("window.scrollTo(0, {})".format(position))
        sources.append(driver.page_source)
        time.sleep(0.3)
        position += 700
    product_list = (make_soup(source).find_all("div", class_="product")
                    for source in sources)
    items = []
    for l in product_list:
        items.extend(filter(bool, map(parse_product, l)))
    return items
