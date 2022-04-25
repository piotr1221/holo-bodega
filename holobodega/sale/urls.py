from django.urls import path
from sale.views import *

urlpatterns = [
    path('products/', products),
    path('cart/', cart),
    path('sell/', sell),
    path('debt/', debt),
    path('debt/edit/<id>',debt_edit,name="debt_edit")
]