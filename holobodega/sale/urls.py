from django.urls import path
from sale.views import *

urlpatterns = [
    path('products/', products),
    path('cart/', cart),
]