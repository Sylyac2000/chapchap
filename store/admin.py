from django.contrib import admin

# Register your models here.
from store.models import Store, Category, Product

admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Product)