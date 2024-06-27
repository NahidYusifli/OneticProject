from django.db import models
from services.mixins import DateMixin
from services.uploader import Uploader
from mptt.models import MPTTModel, TreeForeignKey



class Category(DateMixin, MPTTModel):
    name = models.CharField(max_length=150, unique=True)
    icon = models.ImageField(upload_to=Uploader.category_uploader, blank=True, null=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    

