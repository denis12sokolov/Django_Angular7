import re
import time
import urllib.parse as urlparse
from itertools import chain
from urllib.parse import urlencode

from selenium.common.exceptions import NoSuchElementException
from core.parser.helpers import make_soup, get_down_adidas, get_type_by_name

PRICE = re.compile(r"(\$)|(\xa0)|(\s)")
NUM_PAGE = re.compile(r"(\d+)")


def get_main_price(product):
    element = product.find("span", class_="baseprice")
    if element:
        return PRICE.sub('', element.get_text())


def get_discount_price(product):
    element = product.find("span", class_="salesprice")
    if element:
        return PRICE.sub('', element.get_text())


def get_product_name(product):
    element = product.find("span", class_="title")
    if element:
        return element.get_text()


def get_image_url(product):
    img_element = product.find("img")
    if img_element:
        return img_element.attrs["data-original"]


def get_original_url(product):
    element = product.find("a", class_="product-link")
    if element:
        return element.attrs["href"]


def parse_product(product):
    price = get_main_price(product)
    discount_price = get_discount_price(product)
    product_name = get_product_name(product)
    parsed_product = {
        "list_price": price if price else discount_price,
        "discount_price": discount_price,
        "name": product_name,
        "url_img": get_image_url(product),
        "product_type": get_type_by_name(product_name),
        "url_original": "https://www.reebok.ca" + get_original_url(product),
    }
    return parsed_product


def get_num_pages(driver):
    try:
        num_pages = driver.find_element_by_class_name("paging-total")
        num = NUM_PAGE.findall(num_pages.get_attribute("innerHTML"))[0]
        return int(num)
    except:
        return 1


def to_next_page(driver):
    try:
        next_page = driver.find_element_by_class_name("next")
        next_page.click()
    except NoSuchElementException:
        pass


def get_link_to_next_page(url, num_page):
    num = 120 * (num_page - 1)
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(start=num, sz=120)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


def set_grid_to_largest(driver):
    url = driver.current_url
    param = {"sz": 120}
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(param)
    url_parts[4] = urlencode(query)
    driver.get(urlparse.urlunparse(url_parts))


def parse_reebok_page(driver, url):
    driver.get(url)
    driver.implicitly_wait(15)
    time.sleep(5)
    set_grid_to_largest(driver)
    url = driver.current_url
    num_pages = get_num_pages(driver)
    get_down_adidas(driver, 25)
    sources = [driver.page_source]
    for i in range(2, num_pages + 1):
        driver.get(get_link_to_next_page(url, i))
        time.sleep(2)
        get_down_adidas(driver, 25)
        sources.append(driver.page_source)
    product_list = [make_soup(source).find_all("div", class_="innercard")
                    for source in sources]
    product_list = chain(*product_list)
    return map(parse_product, product_list)
