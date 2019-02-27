import logging
import re
import sys
import time
import urllib.parse as urlparse
from itertools import chain
from urllib.parse import urlencode

from selenium.webdriver.chrome.webdriver import WebDriver

from core.parser.grabber import hide_webdriver, get_chrome_driver, get_firefox_driver
from core.parser.helpers import make_soup, get_down_adidas, get_type_by_name, get_down_adidas2, test_adidas_down

PRICE = re.compile(r"(\$)|(\xa0)|(\s)")
NUM_PAGE = re.compile(r"(\d+)")
size_page = 120
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


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
        return img_element.attrs['src']


def get_original_url(product):
    element = product.find("a", class_="plp-image-bg-link")
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
        "url_img": get_image_url(product).split("?")[0],
        "product_type": get_type_by_name(product_name),
        "url_original": "https://www.adidas.ca" + get_original_url(product),
    }
    return parsed_product


def get_num_pages(driver):
    try:
        num_pages = driver.find_element_by_class_name("paging-total")
        num = NUM_PAGE.findall(num_pages.get_attribute("innerHTML"))[0]
        return int(num)
    except:
        return 1


def to_next_page(driver: WebDriver):
    # hide_webdriver(driver)
    driver.execute_script('document.getElementsByClassName("pagging-next-page")[0].click()')
    # hide_webdriver(driver)
    # dropdown = driver.find_element_by_class_name("ffSelectButton")
    # dropdown.click()
    # page_option = driver.find_element_by_xpath('//span[@data-val="{}"]'.format(page))
    # page_option.click()
    # next_page = driver.find_element_by_class_name("next")
    # next_page.click()


def get_link_to_next_page(url, num_page):
    num = size_page * (num_page - 1)
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(start=num, sz=size_page)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


def get_url_largest(url):
    param = {"sz": size_page}
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(param)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


def parse_adidas_page(driver: WebDriver, url):
    driver.get(get_url_largest(url))
    time.sleep(3)
    logging.info("Get Down")
    test_adidas_down(driver, 20)
    logging.info("Get Down")
    url = driver.current_url
    logging.info("Get Url")
    num_pages = get_num_pages(driver)
    logging.info("Get Num Pages")
    sources = [driver.page_source]
    logging.info("Get Source")
    for i in range(2, num_pages+1):
        link = get_link_to_next_page(url, i)
        logging.info("Get Link To Next Page")
        driver.get(link)
        logging.info("Move to Link to Next Page")
        time.sleep(3)
        test_adidas_down(driver, 20)
        logging.info("Get Down")
        sources.append(driver.page_source)
        logging.info("Append source")
    driver.close()
    driver.quit()
    logging.info("Close Driver")
    logging.info("Start make_soup")
    product_list = [make_soup(source).find_all("div", class_="innercard")
                    for source in sources]
    logging.info("End make_soup")
    product_list = chain(*product_list)
    logging.info("Start parse all source")
    return map(parse_product, product_list)
