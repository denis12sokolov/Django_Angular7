#!/usr/bin/env python3
import traceback

from celery.utils.log import get_task_logger

from core.models import Product, Link
from core.parser.grabber import get_firefox_driver, get_chrome_driver
from core.parser.parsers.adidas_parser import parse_adidas_page
from core.parser.parsers.all_saints_parser import parse_all_saints
from core.parser.parsers.asos_parser import parse_asos_page
from core.parser.parsers.cham_parser import parse_champion_page
from core.parser.parsers.ck_parser import parse_all_ck
from core.parser.parsers.guess_parser import parse_guess_page
from core.parser.parsers.reebok_parser import parse_reebok_page
from core.parser.parsers.tommy_parser import parse_tommy_page
from core.parser.parsers.topman_parser import parse_topman_page
from core.parser.parsers.zara_parser import parse_zara_page

# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = get_task_logger(__name__)

map_shop_name_to_func_parse = {
    "ASOS": parse_asos_page,
    "ADIDAS": parse_adidas_page,
    "CHAMPION": parse_champion_page,
    "TOMMY": parse_tommy_page,
    "ZARA": parse_zara_page,
    "TOPMAN": parse_topman_page,
    "GUESS": parse_guess_page,
    "REEBOK": parse_reebok_page,
    "ALLSAINTS": parse_all_saints,
    "CK": parse_all_ck,
}

map_shop_name_to_driver = {
    "ASOS": "firefox",
    "ADIDAS": "adidas",
    "CHAMPION": "firefox",
    "TOMMY": "chrome",
    "ZARA": "chrome",
    "TOPMAN": "chrome",
    "GUESS": "chrome",
    "REEBOK": "firefox",
    "ALLSAINTS": "firefox",
    "CK": "firefox",
}

shops_all = tuple(map_shop_name_to_func_parse.keys())


def parse_shop(link_type, driver):
    items = []
    old_products = list(Product.objects.filter(link__link_type=link_type).values_list("pk", flat=True))
    parse_func = map_shop_name_to_func_parse[link_type]
    links = Link.objects.filter(link_type=link_type).values_list("url", "shop_name", "id")
    logger.info("Start parse {}. Links: {}".format(link_type, len(links)))
    sum_len = 0
    for url, shop_name, link_id in links:
        try:
            for item in parse_func(driver, url):
                if item.get('url_original'):
                    item.update(shop_name=shop_name, link_id=link_id)
                    items.append(Product(**item))
            Product.objects.bulk_create(items)
            sum_len += len(items)
            items.clear()
        except Exception:
            print(traceback.format_exc())
            logger.warning("Item is skipped")
    logger.info("Number {} items: {}".format(link_type, sum_len))
    Product.objects.filter(pk__in=old_products).delete()



# def parse_ck():
#     shop_product = list(Product.objects.filter(shop_name="CK").values_list("pk", flat=True))
#     links = Link.objects.filter(link_type="CK").values_list("url", flat=True)
#     logging.info("Start parse {}. Links: {}".format("CK", len(links)))
#     items = []
#     for source in grab_ck(links):
#         print(source)
#         try:
#             items = [Product(**item) for item in parse_ck_page(source)]
#         except:
#             print(traceback.format_exc())
#             logging.warning("Item is skipped")
#     logging.info("Number {} items: {}".format("CK", len(items)))
#     Product.objects.bulk_create(items)
#     Product.objects.filter(pk__in=shop_product).delete()


def parse_all(shops=shops_all):
    ff_driver = get_firefox_driver()
    ch_driver = get_chrome_driver()
    ad_driver = get_firefox_driver() if "ADIDAS" in shops else None
    drivers = {
        "firefox": ff_driver,
        "chrome": ch_driver,
        "adidas": ad_driver,
    }

    for shop in shops:
        driver_name = map_shop_name_to_driver[shop]
        parse_shop(shop, drivers[driver_name])

    ff_driver.close()
    ff_driver.quit()
    ch_driver.close()
    ch_driver.quit()


def main():
    parse_all()


if __name__ == '__main__':
    main()
