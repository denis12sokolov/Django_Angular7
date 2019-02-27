from django.contrib import admin
from django.utils.html import format_html

from core.models import Product, Link, ProductType, SubCategory, MapSubcategory, FAQContent, Currency


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    def original_url_field(self, obj: Product):
        dots = '...' if len(obj.url_original) > 80 else ''
        return format_html('<a target="_blank" href="{0}">{1}</a>', obj.url_original, obj.url_original[:80] + dots)
    original_url_field.short_description = 'Original Link'

    def get_shop_name(self, obj: Product):
        return obj.link.shop_name
    get_shop_name.short_description = 'Shop Name'

    list_display = ('get_shop_name', 'name', 'original_url_field', 'product_type')
    search_fields = ('get_shop_name', 'name')
    list_editable = ['product_type']

    def get_changelist_formset(self, request, **kwargs):
        form = super().get_changelist_formset(request, **kwargs)
        form.form.base_fields["product_type"].required = False
        return form


@admin.register(Link)
class LinksAdmin(admin.ModelAdmin):
    list_display = ('url', 'link_type', 'shop_name')
    list_editable = ['shop_name']

    def get_changelist_formset(self, request, **kwargs):
        form = super().get_changelist_formset(request, **kwargs)
        form.form.base_fields["shop_name"].required = False
        return form


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    pass


class MapSubcategoryInline(admin.TabularInline):
    model = MapSubcategory


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'big_type',)
    inlines = [MapSubcategoryInline]


@admin.register(MapSubcategory)
class MapSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory',)


@admin.register(FAQContent)
class FAQContentAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass
