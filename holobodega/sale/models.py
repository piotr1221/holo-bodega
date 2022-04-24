from django.db import models
from inventory.models import Product
# Create your models here.

class Sale(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0)
    products = models.ManyToManyField(Product, through='SaleLine')
    sold = models.BooleanField(default=False)

    def get_sale_lines(self):
        return SaleLine.objects.filter(sale=self).order_by('product__name')

    def get_sale_line_by_product(self, product):
        return SaleLine.objects.filter(sale=self, product=product).all()

    def update_total(self):
        sale_lines = SaleLine.objects.filter(sale=self).all()
        if not sale_lines:
            self.total = 0
        else :
            a = [
                sale_line.amount
                for sale_line
                in sale_lines
            ]
            self.total = sum([
                sale_line.amount
                for sale_line
                in sale_lines
            ])
        self.save()
        return self.total

class SaleLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.product} * {self.quantity} = {self.amount}'

    def add(self):
        self.quantity += 1
        self.amount += self.product.price
        self.save()
        self.sale.update_total()

    def remove(self):
        if self.quantity > 0:
            self.quantity -= 1
            self.amount -= self.product.price
            self.save()
            self.sale.update_total()

class Debtor(models.Model):
    name = models.CharField(max_length=50)
    total_debt = models.DecimalField(max_digits=5, decimal_places=2)

class DebtSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    debtor = models.ForeignKey(Debtor, on_delete=models.PROTECT)
    debt_amount = models.DecimalField(max_digits=5, decimal_places=2)