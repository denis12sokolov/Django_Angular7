from django.db import models

from core.parser.helpers import map_name_product_to_type

ASOS = 'ASOS'
ADIDAS = 'ADIDAS'
CHAMPION = 'CHAMPION'
TOMMY = 'TOMMY'
ZARA = 'ZARA'
TOPMAN = 'TOPMAN'
CK = 'CK'
GUESS = 'GUESS'
REEBOK = 'REEBOK'
ALL_SAINTS = 'ALLSAINTS'
NIKE = 'NIKE'

LINK_TYPES = (
    (ASOS, 'ASOS'),
    (ADIDAS, 'Adidas'),
    (CHAMPION, 'Champion'),
    (TOMMY, 'Tommy Hilfiger'),
    (ZARA, 'Zara'),
    (TOPMAN, 'Topman'),
    (CK, 'Calvin Klein'),
    (GUESS, 'Guess'),
    (REEBOK, 'Reebok'),
    (NIKE, 'Nike'),
    (ALL_SAINTS, 'AllSaints'),
)

PRODUCT_TYPES = tuple(
    (v, v) for v in set(map_name_product_to_type.values())
)


class Link(models.Model):
    STUSSY = "STUSSY"
    FILA = "FILA"
    KAPPA = "KAPPA"
    TOMMY = "TOMMY"
    CK = "CK"
    GUESS = "GUESS"
    FRED_PERRY = "FRED_PERRY"
    VANS = "VANS"
    NIKE = "NIKE"
    ADIDAS = "ADIDAS"
    REEBOK = "REEBOK"
    ALLSAINTS = "ALLSAINTS"
    HM = "HM"
    RALPH_LAUREN = "RALPH_LAUREN"
    TOPMAN = "TOPMAN"
    CHAMPION = "CHAMPION"
    ZARA = "ZARA"

    SHOP_NAME = (
        (STUSSY, "Stussy"),
        (FILA, "Fila"),
        (KAPPA, "Kappa"),
        (TOMMY, "Tommy Hilifiger"),
        (CK, "Calvin Klein"),
        (GUESS, "Guess"),
        (FRED_PERRY, "Fred Perry"),
        (VANS, "Vans"),
        (NIKE, "Nike "),
        (ADIDAS, "Adidas"),
        (REEBOK, "Reebok"),
        (ALLSAINTS, "All Saints"),
        (HM, "H&M"),
        (RALPH_LAUREN, "Ralph Lauren "),
        (TOPMAN, "Topman"),
        (CHAMPION, "Champion"),
        (ZARA, "Zara"),
    )

    MEN = "M"
    WOMEN = "W"
    SEX = (
        (MEN, "Men"),
        (WOMEN, "W"),
    )

    url = models.URLField(unique=True)
    link_type = models.TextField(choices=LINK_TYPES)
    shop_name = models.TextField(choices=SHOP_NAME, null=True)
    sex = models.TextField(choices=SEX)

    def __str__(self):
        return self.url


class ProductType(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    big_type = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING, related_name="subcategories")
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class MapSubcategory(models.Model):
    name = models.CharField(max_length=300)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING, related_name="map_subcategories")

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.CharField(max_length=300, null=True, choices=PRODUCT_TYPES)
    category = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING, null=True)
    url_img = models.URLField(max_length=1000)
    url_original = models.URLField(max_length=1000)
    list_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.TextField()
    shop_name = models.TextField(choices=Link.SHOP_NAME)
    link = models.ForeignKey(to=Link, on_delete=models.DO_NOTHING)


class FAQContent(models.Model):
    question = models.TextField()
    answer = models.TextField()


class Currency(models.Model):
    currency_from = models.TextField()
    currency_to = models.TextField()
    value = models.DecimalField(decimal_places=3, max_digits=10)
    timestamp = models.DateTimeField(auto_now=True)
