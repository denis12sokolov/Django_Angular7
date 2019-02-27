import re
import time

from selenium.common.exceptions import NoSuchElementException

from core.parser.helpers import get_type_by_name, make_soup

PRICE = re.compile(r"(£)|(\xa0)|(RRP)|(\s)")


def get_main_price(product):
    try:
        element = product.find("span", class_="_342BXW_")
    except:
        return None
    return PRICE.sub('', element.text)


def get_discount_price(product):
    try:
        element = product.find("span", class_="JW3hTZk")
    except:
        return None
    return PRICE.sub('', element.text)


def get_element_name(product):
    element = product.find("div", class_="_10-bVn6")
    if element:
        return element.get_text()


def get_image_url(product):
    img_element = product.find("img")
    if img_element:
        return img_element.attrs['src']
    # img_element = element.find_element_by_class_name("_1FN5N-P").find_element_by_tag_name("img")
    # return img_element.get_attribute("src")


def get_original_url(product):
    element = product.find("a", class_="_3x-5VWa")
    if element:
        return element.attrs["href"]
    # element = product.find_element_by_class_name("_3x-5VWa")
    # return element.get_attribute("href")


def parse_product(product):
    try:
        product_name = get_element_name(product)
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
        pass


def load_more(driver):
    try:
        more_button = driver.find_element_by_class_name("_2HG66Ah")
        driver.execute_script("arguments[0].click();", more_button)
        load_more(driver)
    except NoSuchElementException:
        pass


def parse_asos_page(driver, url):
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(7)
    load_more(driver)
    driver.execute_script("window.scrollTo(0, 40000)")
    time.sleep(10)
    source = driver.page_source
    product_list = make_soup(source).find_all(class_="_2oHs74P")
    return map(parse_product, product_list)
