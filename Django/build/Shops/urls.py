from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import cache_page

from core.views import ProductsView, ShopView, CategoriesView, LinksView, ProductCreateView, MapSubcategoriesView, \
    FAQContentView, CurrencyView

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/product/', cache_page(60 * 5)(ProductsView.as_view())),
    path('api/shop/', cache_page(60 * 5)(ShopView.as_view())),
    path('api/categories/', CategoriesView.as_view()),
    path('api/map_categories/', MapSubcategoriesView.as_view()),
    path('api/links/', LinksView.as_view()),
    path('api/parser_data/', ProductCreateView.as_view({'get': 'list'})),
    path('api/faq/', FAQContentView.as_view()),
    path('api/currency/', CurrencyView.as_view()),
]
