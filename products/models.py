from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=50,default='')
    tags = models.CharField(max_length=50,default='')
    handle =models.CharField(max_length=44, default='')
    body = models.CharField(max_length=55, default='')


    def __str__(self):
        return self.title


class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="variants")
    title = models.CharField(max_length=25, default='')
    sku = models.CharField(max_length=25, default='')
    barcode = models.CharField(max_length=25, default='')
    quantity = models.IntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    discount_price = models.PositiveIntegerField(default=0)



    def __str__(self):
        return self.title  + " | " + str(self.product)