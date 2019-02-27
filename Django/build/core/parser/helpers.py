import logging
import sys
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def is_bottom(driver):
    return driver.execute_script("return (window.innerHeight + window.scrollY) >= document.body.offsetHeight")


def make_soup(html):
    return BeautifulSoup(html, 'lxml')


def get_down_tommy(driver):
    time.sleep(2)
    for i in range(3):
        driver.execute_script("window.scrollTo(0, 40000)")
        time.sleep(2)


def get_down_topman(driver, repeat=3):
    for _ in range(repeat):
        driver.execute_script("window.scrollTo(0, 400000)")
        time.sleep(0.3)


def get_down_adidas(driver, repeat=3):
    time.sleep(2)
    logging.info("Start finding body tag")
    for _ in range(5):
        try:
            body = driver.find_element_by_tag_name('body')
            break
        except:
            pass
    else:
        return
    logging.info("Start Push PAGE_DOWN Key")
    for _ in range(repeat):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
        close_modal_adidas(driver)


def test_adidas_down(driver, repeat=3):
    position = 0
    logging.info("Start test_adidas_down")
    for _ in range(50):
        driver.execute_script("window.scrollTo(0, {})".format(position))
        time.sleep(0.2)
        close_modal_adidas(driver)
        position += 700


def close_modal_adidas(driver):
    try:
        driver.execute_script('document.getElementsByClassName("ui-dialog-titlebar-close")[0].click()')
    except:
        pass


def get_down_adidas2(driver):
    body = driver.find_element_by_tag_name('body')
    while not is_bottom_adidas(driver):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.8)
        close_modal_adidas(driver)


map_name_product_to_type2 = {
    "t-shirt": "t-shirt",
    "polo": "polo",
    "tee": "t-shirt",
    "hoodie": "hoodie",
    "jumper": "jumper",
    "jogger": "jogger",
    "tank": "tank",
    "top": "top",
    "knit": "knit",

    "shirt": "shirt",
    "oxford": "shirt",

    "sneaker": "sneaker",
    "runner": "sneaker",
    "boot": "boot",
    "trainers": "sneaker",
    "loafer": "boot",
    "plimsolls": "boot",
    "shoe": "shoe",
    "slip on": "shoe",
    "slippers": "shoe",

    "bag": "accessory",
    "cap": "accessory",
    "aviators": "accessory",
    "sunglasses": "accessory",
    "pouch": "accessory",
    "square": "accessory",
    "belt": "accessory",
    "backpack": "accessory",
    "scarf": "accessory",
    "headband": "accessory",
    "tie": "accessory",
    "hoops": "accessory",
    "watch": "accessory",
    "snood": "accessory",
    "socks": "accessory",
    "pin": "accessory",
    "necklace": "accessory",
    "rucksack": "accessory",
    "holdall": "accessory",
    "wallet": "accessory",
    "cardholder": "accessory",
    "tote": "accessory",
    "chain": "accessory",
    "earrings": "accessory",
    "collar": "accessory",

    "short": "short",
    "shorts": "short",
    "bermuda": "short",

    "sweatpant": "pant",
    "pant": "pant",
    "jean": "jean",
    "chino": "jean",
    "leggings": "pant",

    "trunk": "underwear",
    "trouser": "underwear",
    "briefs": "underwear",
    "bra": "underwear",

    "windbreaker": "outerwear",
    "bomber": "outwear",
    "jacket": "outwear",
    "coat": "outwear",
    "gilet": "outwear",
    "vest": "outwear",
    "hood": "outwear",
    "parka": "outwear",
    "shacket": "outwear",
    "kimono": "outwear",
    " mac": "outwear",
    "poncho": "outwear",

    "cardigan": "cardigan",
    "sweater": "sweater",
    "sweatshirt": "sweatshirt",

    "suit": " suit",
    "blazer": "blazer",

    "hat": "hat",
    "beanie": "hat",
    "snapback": "hat",
}
map_name_product_to_type = {
    "polo": "polo",

    "t-shirt": "t-shirt",
    "tee": "t-shirt",

    "long-sleeve": "long-sleeves",
    "longsleeve": "long-sleeves",

    "tank": "tank-tops",
    "tank-top": "tank-tops",

    "knit": "cardigans",
    "cardigan": "cardigans",

    "crewneck": "crewnecks",
    "jumper": "crewnecks",

    "hoodie": "Hoodies-and-Zipups",
    "zipup": "Hoodies-and-Zipups",

    "sweatshirt": "sweatshirts",

    "turtleneck": "turtlenecks",

    "bomber": "bombers",

    "windbreaker": "jackets",
    "jacket": "jackets",
    "parka": "jackets",
    "shacket": "jackets",
    "mac": "jackets",
    "poncho": "jackets",
    "jean-jacket": "jackets",
    "denim-jacket": "jackets",

    "coat": "coats",

    "vest": "vests",
    "gilet": "vests",

    "pants": "pants",
    "chino": "pants",
    "trouser": "trousers",

    "sweatpants": "sweatpants",

    "jogger": "joggers",

    "jeans": "jeans",

    "shorts": "shorts",

    "dress-shirt": "dress-shirt",
    "blouse": "dress-shirt",

    "dress-pants": "dress-pants",

    "suit": "suits",

    "blazer": "blazers",

    "sneaker": "sneakers",
    "trainer": "sneakers",
    "runner": "sneakers",

    "loafer": "loafers",
    "plimsoll": "loafers",
    "slip-on": "loafers",

    "slippers": "loafers",

    "belt": "belts",

    "hat": "hats",
    "cap": "hats",
    "snapback": "hats",
    "toque": "hats",
    "beanie": "hats",

    "gloves": "gloves",
    "mittens": "gloves",

    "jewelry": "jewelry",
    "necklace": "jewelry",
    "bracelet": "gloves",
    "earring": "jewelry",
    "watch": "jewelry",

    "scarf": "scarves",

    "bag": "backpacks",
    "backpack": "backpacks",
    "napsack": "backpacks",

    "sock": "socks",

    "wallet": "wallets",

    "pins": "other",
    "pin": "other",
    "keychain": "other",
    "lighter": "other",

    "glasses": "eyewear",
    "aviator": "eyewear",
    "sunglasses": "eyewear",

    "ties": "formal-wear",

    "boxers": "boxers",
    "briefs": "boxers",

    "bra": "bras",

    "brief": "briefs",

    "corset": "corsets-and-bodysuits",
    "bodysuit": "corsets-and-bodysuits",

    "thong": "thongs",
}
keys = list(map_name_product_to_type.keys())


def get_type_by_name(name: str):
    name = name.lower()
    for k in keys:
        if k in name:
            return map_name_product_to_type[k]


def is_bottom_adidas(driver):
    try:
        return driver.execute_script(
            "return (window.innerHeight + window.scrollY) >= document.getElementById('container').offsetHeight")
    except:
        return False
