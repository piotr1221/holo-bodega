from django.urls import path
from inventory.views import *

urlpatterns = [
    # PRODUCTOS
    path('product/', products),
    path('new_product/', new_product),
    path('product/delete/<id>/',delete_product,name="delete_product"),
    path('product/search/',search_product,name="search_product"),
    #CATEGORÍAS
    path('new_category', new_category),
    path('category/', categories),
    path('category/delete/<id>/',delete_category,name="delete_category"),
    path('category/search/',search_category,name="search_category")
]