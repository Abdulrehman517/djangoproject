from django.db import models
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255,null=True, blank=True)
    tags = models.CharField(max_length=500,null=True, blank=True)
    handle =models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Variant(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prod_var")
    title = models.CharField(max_length=255,blank=True,null=True)
    sku = models.CharField(max_length=255,null=True, blank=True)
    barcode = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title