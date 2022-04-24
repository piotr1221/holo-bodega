from django.urls import path
from inventory.views import *


urlpatterns = [
    path('category/', categories),
    path('product/', products),
]