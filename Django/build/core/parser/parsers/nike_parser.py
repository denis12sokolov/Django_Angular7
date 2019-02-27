import re
import time

from core.parser.helpers import make_soup, get_down_topman, get_type_by_name

PRICE = re.compile(r"(\$)|(\xa0)|(\s)")


def get_main_price(product):
    element = product.find("span", class_="overridden")
    if element:
        return PRICE.sub('', element.get_text())


def get_discount_price(product):
    element = product.find("span", class_="local")
    if element:
        return PRICE.sub('', element.get_text())


def get_product_name(product):
    element = product.find("p", class_="product-display-name")
    if element:
        return element.get_text()


def get_image_url(product):
    img_element = product.find("img")
    if img_element:
        return img_element.attrs['src']


def get_original_url(product):
    element = product.find("a")
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
        "url_original": get_original_url(product),
    }
    return parsed_product


def parse_nike_page(driver, url):
    driver.get(url)
    driver.implicitly_wait(15)
    time.sleep(5)
    get_down_topman(driver, 50)
    source = driver.page_source
    product_list = make_soup(source).find_all("div", class_="grid-item")
    return map(parse_product, product_list)
