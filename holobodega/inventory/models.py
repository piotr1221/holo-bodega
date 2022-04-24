from django.db import models
# from sale.models import *

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

class Producer(models.Model):
    name = models.CharField(max_length=50)

class Product(models.Model):
    name = models.CharField(max_length=50)
    producer = models.ForeignKey(Producer, on_delete=models.PROTECT)
    barcode = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    stock = models.BigIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.name} {self.category.name} {self.price}'

    # def get_sale_line_quantity_from_order(self, order):
    #     return SaleLine.objects.filter(product=self, order=order).first().quantity