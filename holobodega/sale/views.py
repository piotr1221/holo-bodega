from django.shortcuts import render
from django.db.models import *
from sale.models import *

# Create your views here.

def products(req):
    category = req.GET.get('category', '')
    name = req.GET.get('name', '')
    update = req.GET.get('update', '')
    id = req.GET.get('id', '')

    products = Product.objects
    if category:
        products = products.filter(category__name=category)

    if name:
        products = products.filter(name__icontains=name)
    
    products = products.all().annotate(quantity=Value(0, output_field=IntegerField()))

    sale = update_sale(req, product_id=id, update=update)

    for product in products:
        for line in sale.get_sale_lines():
            if product.id == line.product.id:
                product.quantity = line.quantity

    context = {
        'products': products,
    }
    return render(req, 'sale/products.html', context)

def update_sale(req, *, product_id, update):
    sale = Sale.objects.filter(sold=False).first()
    if sale is None:
        sale = Sale.objects.create()
    
    if not product_id:
        return sale

    product = Product.objects.get(id=product_id)
    sale_line = SaleLine.objects.filter(sale=sale, product=product).first()
    
    if sale_line is None:
        sale_line = SaleLine.objects.create(
                        product=product,
                        sale=sale,
                    )

    if update == 'add':
        sale_line.add()
    elif update == 'remove':
        sale_line.remove()

    if sale_line.quantity == 0:
        sale_line.delete()

    return sale

def cart(req):
    update = req.GET.get('update', '')
    id = req.GET.get('id', '')
    sale = update_sale(req, product_id=id, update=update)
    context = {
        'sale': sale
    }
    return render(req, 'sale/cart.html', context)
