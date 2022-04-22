from django.db import models
from inventory.models import Product
# Create your models here.

class Sale(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    products = models.ManyToManyField(Product, through='SaleLine')

class SaleLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()

class Debtor(models.Model):
    name = models.CharField(max_length=50)
    total_debt = models.DecimalField(max_digits=5, decimal_places=2)

class DebtSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    debtor = models.ForeignKey(Debtor, on_delete=models.PROTECT)
    debt_amount = models.DecimalField(max_digits=5, decimal_places=2)