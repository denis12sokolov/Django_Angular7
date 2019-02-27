import re
import time
from itertools import chain

from selenium.common.exceptions import NoSuchElementException

from core.parser.helpers import make_soup, get_down_tommy, get_type_by_name

PRICE = re.compile(r"(\$)|(\xa0)|(\s)")


def get_main_price(product):
    element = product.find("span", class_="listPrice")
    if element:
        return PRICE.sub('', element.get_text())


def get_discount_price(product):
    element = product.find("span", class_="offerPrice")
    if element:
        return PRICE.sub('', element.get_text())


def get_product_name(product):
    element = product.find("a", class_="link")
    if element:
        return element.get_text()


def get_image_url(product):
    img_element = product.find("img")
    if img_element:
        return img_element.attrs['src']


def get_original_url(product):
    element = product.find("a", class_="link")
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


def close_modal(driver):
    try:
        close_x = driver.find_element_by_class_name("pvhOverlayCloseX")
        if close_x:
            close_x.click()
    except NoSuchElementException:
        pass


def get_num_pages(driver):
    try:
        num_pages = driver.find_element_by_class_name("totalPagesMessage")
        return int(num_pages.get_attribute("data-total-pages"))
    except:
        return 1


def to_next_page(driver):
    try:
        next_page = driver.find_element_by_class_name("next")
        next_page.click()
    except NoSuchElementException:
        pass


def get_link_to_next_page(url, num_page):
    return url + r"#page={}".format(num_page)


def parse_tommy_page(driver, url):
    driver.get(url)
    driver.implicitly_wait(15)
    time.sleep(5)
    close_modal(driver)
    get_down_tommy(driver)
    url = driver.current_url
    num_pages = get_num_pages(driver)
    sources = [driver.page_source]
    for i in range(2, num_pages + 1):
        driver.get(get_link_to_next_page(url, i))
        get_down_tommy(driver)
        sources.append(driver.page_source)
    product_list = [make_soup(source).find_all("div", class_="productCell")
                    for source in sources]
    product_list = chain(*product_list)
    return map(parse_product, product_list)
