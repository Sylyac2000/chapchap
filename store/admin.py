from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from store.models import Store, Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'categoryimage_thumbnail')
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'store', 'productimage_thumbnail']
    list_filter = ['name', 'category', 'price', 'store']
    list_editable = ['price',]

    def productimage_thumbnail(self, obj):
        return format_html('<img src="{}" width="100" height="50" />'.format(obj.productimage_thumbnail.url))

    productimage_thumbnail.short_description = 'Image'

admin.site.register(Store)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)