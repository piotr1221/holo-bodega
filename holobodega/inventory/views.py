from django.shortcuts import redirect, render

from inventory.forms import NewProductForm
from inventory.models import Category, Producer, Product

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
