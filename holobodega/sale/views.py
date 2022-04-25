from multiprocessing import context
from xmlrpc.client import Boolean
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import *
from sale.models import *
import decimal
import datetime

# Create your views here.

def products(req):
    category = req.GET.get('category', '')
    name = req.GET.get('search_input', '')
    update = req.GET.get('update', '')
    id = req.GET.get('id', '')

    products = Product.objects
    if category:
        products = products.filter(category__name=category)

    if name:
        products = products.filter(name__icontains=name)
    
    if update == 'cart':
        add_to_cart(product_id=id)

    products = products.all()
    sale = Sale.objects.filter(sold=False).first()

    if sale is not None:
        products = products.annotate(in_current_sale=Value(False, output_field=BooleanField()))
    
        for product in products:
            for line in sale.get_sale_lines():
                if product.id == line.product.id:
                    product.in_current_sale = True

    
    context = {
        'products': products,
    }
    return render(req, 'sale/products.html', context)

def add_to_cart(*, product_id):
    sale = Sale.objects.filter(sold=False).first()
    if sale is None:
        sale = Sale.objects.create()

    if not product_id:
        return

    product = Product.objects.get(id=product_id)
    sale_line = SaleLine.objects.filter(sale=sale, product=product).first()

    if sale_line is None:
        sale_line = SaleLine.objects.create(
                        product=product,
                        sale=sale,
                        amount=product.price
                    )

def update_sale(*, product_id, update):
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
                        amount=product.price
                    )

    if update == 'add':
        sale_line.add()
    elif update == 'remove':
        sale_line.remove()

    if sale_line.quantity == 0 or update == 'delete':
        sale_line.delete()

    return sale

def cart(req):
    update = req.GET.get('update', '')
    id = req.GET.get('id', '')
    sale = update_sale(product_id=id, update=update)
    context = {
        'sale': sale
    }
    return render(req, 'sale/cart.html', context)

def sell(req):
    sale = Sale.objects.filter(id=req.POST.get('sale_id')).first()
    sale.sold = True
    sale.save()
    decrease_stock(req, sale)
    return redirect('/sale/products/')

def decrease_stock(req, sale):
    for sale_line in sale.get_sale_lines():
        sale_line.product.stock -= sale_line.quantity
        sale_line.product.save()
        if (sale_line.product.stock <= 5):
            messages.warning(req, f'Quedan {sale_line.product.stock} unidades del producto {sale_line.product.name}')

def debt(req):
    name = req.GET.get('search_input', '')
    debtors = Debtor.objects
    if name:
        debtors = debtors.filter(name__icontains=name)
    else:
        debtors = debtors.all()

    sale = Sale.objects.filter(sold=False).first()
    if sale is not None:
        cart_present = True
    else:
        cart_present = False

    context = {
        'debtors': debtors,
        'cart_present': cart_present
    }
    return render(req, 'sale/debt.html', context)

def create_debtor(req):
    name = req.POST.get('debtor-name', '')
    Debtor.objects.create(name=name)
    return redirect('debt')

def add_debt_to_debtor(req):
    id = req.POST.get('debtor', '')
    
    debtor = Debtor.objects.filter(id=id).first()
    sale = Sale.objects.filter(sold=False).first()
    debt_sale = DebtSale.objects.create(
        sale=sale,
        debtor=debtor,
        debt_amount=sale.update_total()
    )
    sale.sold = True
    sale.save()
    
    debtor.add_debt(debt_sale)
    decrease_stock(req, sale)
    return redirect('/sale/debt/')

def add_payment_to_debtor(req):
    id = req.POST.get('debtor', '')
    payment = decimal.Decimal(req.POST.get('payment', ''))
    debtor = Debtor.objects.filter(id=id).first()
    debtor.pay_debt(payment)
    return redirect('/sale/debt/')

def debt_edit(req, id):
    debtor=Debtor.objects.filter(id=id).first()
    context = {
        'debtor':debtor
    }
    return render(req, 'sale/debt-edit.html', context)

def cash(req):
    sales = Sale.objects.filter(time__range=(
        datetime.datetime.combine(datetime.date.today(), datetime.time(00, 00, 00)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(23, 59, 59))
    ), sold=True)
    for sale in sales:
        sale.time += datetime.timedelta(hours=-5)
        sale.time = sale.time.strftime("%H:%M %p")

    context = {
        'sales': sales,
        'total': sum([sale.total for sale in sales])
    }
    return render(req, 'sale/sales.html', context)

def sale_detail(req):
    sale = Sale.objects.filter(id=req.GET.get('sale', '')).first()
    context = {
        'sale': sale
    }
    return render(req, 'sale/sale-detail.html', context)