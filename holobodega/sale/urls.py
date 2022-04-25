from unicodedata import name
from django.urls import path
from sale.views import *

urlpatterns = [
    path('products/', products),
    path('cart/', cart),
    path('sell/', sell),
    path('debt/', debt,name="debt"),
    path('debt/create-debtor/', create_debtor),
    path('debt/add-debt/', add_debt_to_debtor),
    path('debt/edit/<id>/', debt_edit, name="debt_edit"),
    path('debt/cancel-debt/', add_payment_to_debtor)
]