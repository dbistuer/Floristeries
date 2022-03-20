from django.shortcuts import render, redirect
from .models import *
# Create your views here.

def listProducts(request):
    productes = Producte.objects.all()
    return render(request, "Product/list.html", {"productes": productes})

def addProduct(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = float(request.POST['price'].replace(",","."))
        product = Producte.objects.create(name=name, description=description, price=price)
        return render(request, 'Product/add.html')
    else:
        return render(request, 'Product/add.html')

def detailProduct(request, id):
    product = Producte.objects.get(id=id)
    json={'product':product}
    return render(request, 'Product/detail.html',json)

def boughtElements(request):
    compra = request.compra
    elements = Elements.objects.get(Compra=compra)
    json={'elements':elements}
    return render(request, 'Compra/show.html')