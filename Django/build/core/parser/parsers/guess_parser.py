import re
import time

from core.parser.helpers import make_soup, get_type_by_name

PRICE = re.compile(r"\d+\.\d{2}")


def get_main_price(product):
    element = product.find("span", class_="priceVal")
    if element:
        return PRICE.search(element.get_text()).group(0)


def get_discount_price(product):
    element = product.find("span", class_="priceVal actual")
    if element:
        return PRICE.search(element.get_text()).group(0)


def get_product_name(product):
    element = product.find("div", class_="name")
    if element:
        return element.get_text().strip().replace('"', '')


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


def parse_guess_page(driver, url):
    driver.get(url)
    driver.implicitly_wait(15)
    time.sleep(15)
    driver.execute_script("window.scrollTo(0, 40000)")
    time.sleep(5)
    source = driver.page_source
    product_list = make_soup(source).find_all("li", class_="product-bucket")
    return map(parse_product, product_list)
