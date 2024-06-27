from django.db import models
from base.models import Category
from ckeditor.fields import RichTextField
from services.mixins import DateMixin
from colorfield.fields import ColorField
# from mptt.models import MPTTModel, TreeForeignKey
from services.generator import CodeGenerator
from services.uploader import Uploader
from services.slugify import slugify
from django.contrib.auth import get_user_model

User = get_user_model()



class Brand(DateMixin):
    brand = models.CharField(max_length=150)
    logo = models.ImageField(Uploader.brand_logo_uploader, blank=True, null=True)
    description = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.brand
    

class Color(DateMixin):
    color = ColorField()

    def __str__(self):
        return self.color
    
    
class Size(DateMixin):
    size = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"
    
    def __str__(self):
        return self.size
    



class Product(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ManyToManyField(Color, blank=True)
    description = RichTextField()
    size = models.ForeignKey(Size, blank=True, null=True, on_delete=models.SET_NULL)
    price = models.FloatField()
    discount_interest = models.IntegerField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    code = models.SlugField(unique=True, editable=False)
    slug = models.SlugField(unique=True, editable=False)


    def __str__(self):
        return self.name
    

    @property
    def total_price(self):
        discount_price = self.price * (self.discount_interest or 0) / 100
        discounted_price = self.price - discount_price
        return round(float(discounted_price), 2)
    
    def create_unique_slug(self, slug, index=0):
        new_slug = slug
        if index:
            new_slug = f"{slug}-{index}"
        qs = self.__class__.objects.filter(slug=new_slug)
        return self.create_unique_slug(slug, index + 1) if qs.exists() else new_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.create_unique_slug(slugify(self.name))
        if not self.code:
            self.code = CodeGenerator().create_product_shortcode(size=8, model_=self.__class__)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"




class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(Uploader.product_image_uploader, blank=True, null=True)

    def __str__(self) -> str:
        return self.product.name
    
    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"






