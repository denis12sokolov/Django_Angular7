import re
import time
import urllib.parse as urlparse
from urllib.parse import urlencode

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver

from core.parser.helpers import make_soup, get_type_by_name

PRICE = re.compile(r"\d+\.\d{2}")


def get_price_from_text(text):
    return float(PRICE.search(text).group(0))


def get_main_price(product):
    element = product.find("span", class_="price")
    if element:
        return get_price_from_text(element.get_text())
    else:
        return 0


def get_discount_price(product):
    element = product.find("span", class_="now")
    if element:
        return get_price_from_text(element.get_text())
    else:
        return 0


def get_product_name(product):
    element = product.find("span", class_="product_name")
    return element.get_text()


def get_image_url(product):
    img_element = product.find("img")
    if img_element:
        return "https:" + img_element.attrs['src']


def get_original_url(product):
    element = product.find("a", class_="mainImg")
    if element:
        return element.attrs["href"]


def parse_product(product):
    product_name = get_product_name(product)
    parsed_product = {
        "list_price": get_main_price(product),
        "discount_price": get_discount_price(product),
        "name": product_name,
        "url_img": get_image_url(product),
        "product_type": get_type_by_name(product_name),
        "url_original": "https://www.ca.allsaints.com" + get_original_url(product),
    }
    return parsed_product


def parse_source(source):
    return make_soup(source).find_all("div", class_="each-product")


def get_url_view(url):
    param = {"view": "all"}
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(param)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


def parse_all_saints(driver: WebDriver, url):
    driver.get(get_url_view(url))
    driver.implicitly_wait(30)
    time.sleep(10)
    try:
        driver.execute_script("window.scrollTo(0, 40000)")
        time.sleep(10)
    except NoSuchElementException:
        pass
    product_list = make_soup(driver.page_source).find_all("div", class_="product")
    return map(parse_product, product_list)
