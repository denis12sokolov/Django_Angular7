import re
import time
from itertools import chain

from selenium.common.exceptions import NoSuchElementException

from core.parser.helpers import make_soup, get_type_by_name

PRICE = re.compile(r"(\$)|(\xa0)|(\s)|(CAD)")
NAME = re.compile(r"([\"'(),])")

name_elements = set()
null_img = "https://static.zara.net/stdstatic/1.85.3-b.3/images/transparent-background.png"


def get_main_price(product):
    element = product.find("span", class_="line-through")
    if element:
        return PRICE.sub('', element.get_text()).replace(",", ".")


def get_discount_price(product):
    element = product.find("span", class_="sale")
    if element:
        return PRICE.sub('', element.get_text()).replace(",", ".")


def get_product_name(product):
    element = product.find("a", class_="name")
    if element:
        return NAME.sub("", element.get_text())


def get_image_url(product):
    img_element = product.find("img", class_="product-media")
    if img_element:
        return img_element.attrs['src']


def get_original_url(product):
    element = product.find("a", class_="name")
    if element:
        return element.attrs["href"]


def parse_product(product):
    img = get_image_url(product)
    product_name = get_product_name(product)
    if 'transparent' not in img and product_name not in name_elements:
        name_elements.add(product_name)
        price = get_main_price(product)
        discount_price = get_discount_price(product)
        if not discount_price:
            discount_price = 0.0
        parsed_product = {
            "list_price": price if price else discount_price,
            "discount_price": discount_price,
            "name": product_name,
            "url_img": "https:" + img,
            "product_type": get_type_by_name(product_name),
            "url_original": get_original_url(product),
        }
        return parsed_product


def set_grid_to_4(driver):
    try:
        grid = driver.find_element_by_class_name("_four")
        grid.click()
    except NoSuchElementException:
        pass


def close_modal(driver):
    try:
        close_x = driver.find_element_by_class_name("fonticon-close")
        if close_x:
            close_x.click()
    except NoSuchElementException:
        pass


def parse_zara_page(driver, url):
    driver.get(url)
    driver.implicitly_wait(15)
    time.sleep(5)
    close_modal(driver)
    set_grid_to_4(driver)
    sources = [driver.page_source]
    position = 700
    for _ in range(40):
        driver.execute_script("window.scrollTo(0, {})".format(position))
        sources.append(driver.page_source)
        time.sleep(0.3)
        position += 700
    product_list = [make_soup(source).find_all("li", class_="product")
                    for source in sources]
    product_list = list(chain(*product_list))
    return filter(bool, map(parse_product, product_list))
