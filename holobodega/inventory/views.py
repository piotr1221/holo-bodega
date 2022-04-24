from django.shortcuts import render
from django.db.models import *
from inventory.models import *

# Create your views here.
def categories (req):
  return render(req, 'inventory/categories.html')

def products (req):
  return render(req, 'inventory/products.html')