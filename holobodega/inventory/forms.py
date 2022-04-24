from django import forms

from inventory.models import Category, Producer, Product

class NewProductForm(forms.ModelForm):
  name = forms.CharField(max_length=50)
  producer = forms.ModelChoiceField(queryset=Producer.objects.all())
  barcode = forms.IntegerField()
  category = forms.ModelChoiceField(queryset=Category.objects.all())
  stock = forms.IntegerField()
  price = forms.DecimalField()

  class Meta:
    model = Product
    fields = ('name', 'producer', 'barcode', 'category', 'stock', 'price')


class NewCategoryForm(forms.ModelForm):
  name = forms.CharField(max_length=50)
