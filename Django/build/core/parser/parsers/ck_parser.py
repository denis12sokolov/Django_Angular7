import logging
import re
import sys
import time
from itertools import chain

from selenium.common.exceptions import NoSuchElementException

from core.parser.helpers import make_soup, get_type_by_name

PRICE = re.compile(r"(\$)|(\xa0)|(\s)|(CAD)")
PRICE_SEARCH = re.compile(r"\d+\.\d{2}")
NAME = re.compile(r"([\"'(),])")
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def get_main_price(product):
    element = product.find("span", class_="listPrice")
    if element:
        price = PRICE.sub('', element.get_text()).replace(",", ".")
        return PRICE_SEARCH.search(price).group(0)


def get_discount_price(product):
    element = product.find("span", class_="offerPrice")
    if element:
        price = PRICE.sub('', element.get_text()).replace(",", ".")
        return PRICE_SEARCH.search(price).group(0)


def get_product_name(product):
    element = product.find("a", class_="link")
    if element:
        return NAME.sub("", element.get_text())


def get_image_url(product):
    img_element = product.find("img")
    if img_element:
        return img_element.attrs['data-src']


def get_original_url(product):
    element = product.find("a", class_="link")
    if element:
        return element.attrs["href"]


def parse_product(product):
    try:
        price = get_main_price(product)
        discount_price = get_discount_price(product)
        product_name = get_product_name(product)
        parsed_product = {
            "list_price": price if price else discount_price,
            "discount_price": discount_price,
            "name": get_product_name(product),
            "url_img": get_image_url(product),
            "product_type": get_type_by_name(product_name),
            "url_original": get_original_url(product),
        }
    except:
        logging.info("Item CK is skipped")
        return None
    return parsed_product


def parse_ck_page(source):
    product_list = make_soup(source).find_all("div", class_="productCell")
    return filter(bool, map(parse_product, product_list))


def get_num_pages(driver):
    try:
        num_pages = driver.find_element_by_class_name("totalPagesMessage")
        return int(num_pages.get_attribute("data-total-pages"))
    except:
        return 1


def close_modal(driver):
    try:
        close_x = driver.find_element_by_class_name("pvhOverlayCloseX")
        if close_x:
            close_x.click()
    except:
        pass


def to_next_page(driver):
    try:
        driver.execute_script("document.getElementsByClassName('next')[0].click()")
        # next_page = driver.find_element_by_class_name("next")
        # next_page.click()
    except:
        pass


def parse_all_ck(driver, url):
    driver.get(url)
    driver.implicitly_wait(15)
    time.sleep(10)
    close_modal(driver)
    driver.execute_script("window.scrollTo(0, 60000)")
    num_pages = get_num_pages(driver)
    logging.info(f"Get {num_pages} pages")
    time.sleep(10)
    sources = [driver.page_source]
    for i in range(2, num_pages + 1):
        to_next_page(driver)
        driver.implicitly_wait(15)
        time.sleep(10)
        driver.execute_script("window.scrollTo(0, 60000)")
        time.sleep(5)
        sources.append(driver.page_source)
    product_list = [make_soup(source).find_all("div", class_="productCell")
                    for source in sources]
    product_list = chain(*product_list)
    return filter(bool, map(parse_product, product_list))
