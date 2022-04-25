from django.urls import path
from inventory.views import *

urlpatterns = [
    # PRODUCTOS
    path('product/', products),
    path('new_product/', new_product),
    path('product/delete/<id>/',delete_product,name="delete_product"),
    path('product/search/',search_product,name="search_product"),
    path('product/add-stock/<id>/',add_stock_to_product,name="add_stock_to_product"),
    path('product/add-stock/<id>/info/',add_stock,name="add_stock"),
    #CATEGORÍAS
    path('new_category/', new_category),
    path('category/', categories),
    path('category/delete/<id>/',delete_category,name="delete_category"),
    path('category/search/',search_category,name="search_category"),
]