from multiprocessing import context
from django.shortcuts import redirect, render,get_object_or_404
from django.db.models import *
from inventory.forms import *
from inventory.models import *
from django.shortcuts import redirect, render

# Create your views here.

def new_product(request):
    if request.method == 'POST':
        form = NewProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            producer = form.cleaned_data.get('producer')
            barcode = form.cleaned_data.get('barcode')
            category = form.cleaned_data.get('category')
            stock = form.cleaned_data.get('stock')
            price = form.cleaned_data.get('price')
            Product.objects.create(name=name, producer=producer, barcode=barcode, category=category, stock=stock, price=price)
            return redirect("")
    else:
        form = NewProductForm()

    categories = Category.objects.all()
    producers = Producer.objects.all()
    
    context = {
        'form': form,
        'categories': categories,
        'producers': producers
    }

    return render(request, 'inventory/product_form.html', context)
    
def categories (req):
  categories=Category.objects.all()
  context ={
    'categories':categories
  }
  return render(req, 'inventory/categories.html',context)

def search_category(req):
  if req.method=='POST':
    name=req.POST.get("search_input")
  categories=Category.objects.filter(name__contains=name)
  context={
    'categories':categories
  }
  return render(req,'inventory/categories.html',context)

def delete_category (req, id):
  category=get_object_or_404(Category,id=id)
  category.delete()
  return redirect(categories)

def delete_product (req, id):
  product=get_object_or_404(Product,id=id)
  product.delete()
  return redirect(products)

def products (req):
  products=Product.objects.all()
  context ={
    'products':products
  }
  return render(req, 'inventory/products.html',context)

def search_product(req):
  if req.method=='POST':
    name=req.POST.get("search_input")
  products=Product.objects.filter(name__contains=name)
  context={
    'products':products
  }
  return render(req,'inventory/products.html',context)

def new_category(request):
    if request.method == 'POST':
        form = NewCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            Category.objects.create(name=name)
            return redirect("")
    else:
        form = NewCategoryForm()
    
    context = {
        'form': form
    }

    return render(request, 'inventory/category_form.html', context)
