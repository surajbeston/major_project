from django.db import models

from django.db.models import CharField
from django.db.models.functions import Lower

CharField.register_lookup(Lower)


class Product(models.Model):
    name = models.CharField(max_length= 10000)
    description = models.TextField(blank = True, null = True)
    image = models.CharField(max_length = 1000)
    price = models.FloatField(default = 0)
    category = models.CharField(max_length = 300)
    category_slug = models.CharField(max_length=400, null = True, blank = True)
    sub_category = models.CharField(max_length = 300)
    sub_category_slug = models.CharField(max_length = 400, null = True, blank = True)
    brand = models.CharField(max_length = 200, null = True, blank = True)
    url = models.URLField(null = True, blank = True, max_length=1000)
    ecommerce = models.CharField(max_length= 200)

    def __str__(self):
        return self.name
