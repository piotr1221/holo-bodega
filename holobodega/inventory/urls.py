from django.urls import path
from inventory.views import *

urlpatterns = [
    # PRODUCTOS
    path('new_product/', new_product),
    #CATEGORÍAS
    # path('new_category', new_category),
]