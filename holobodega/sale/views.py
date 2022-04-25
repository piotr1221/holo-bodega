from multiprocessing import context
from xmlrpc.client import Boolean
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import *
from sale.models import *
import decimal

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
    return redirect('/sale/products')

def debt(req):
    name = req.GET.get('search_input', '')
    debtors = Debtor.objects
    if name:
        debtors = debtors.filter(name__icontains=name)
    else:
        debtors = debtors.all()

    context = {
        'debtors': debtors
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
    return redirect('/sale/debt/')

def add_payment_to_debtor(req):
    id = req.POST.get('debtor', '')
    payment = decimal.Decimal(req.POST.get('payment', ''))
    debtor = Debtor.objects.filter(id=id).first()
    debtor.pay_debt(payment)
    return redirect('/sale/debt/')

def debt_edit(req,id):
    debtor=Debtor.objects.filter(id=id).first()
    context={
        'debtor':debtor
    }
    return render(req,'sale/debt-edit.html',context)
