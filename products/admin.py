from django.contrib import admin
from .models import Product, Brand, Color, ProductImage


class ImageInline(admin.StackedInline):
    model = ProductImage
    extra = 2

class ProductAdmin(admin.ModelAdmin):
    inlines = (ImageInline, )



admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(ProductImage)
