from django.db import models
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=50,default='')
    tags = models.CharField(max_length=50,default='')
    handle =models.CharField(max_length=44, default='')
    body = models.CharField(max_length=55, default='')


    def __str__(self):
        return self.title


class Variant(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prod_var")
    title = models.CharField(max_length=25, default='')
    sku = models.CharField(max_length=25, default='')
    barcode = models.CharField(max_length=25, default='')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title