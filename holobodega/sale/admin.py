from django.contrib import admin

from sale.models import *

# Register your models here.
admin.site.register(Debtor)
admin.site.register(DebtSale)
admin.site.register(Sale)
admin.site.register(SaleLine)