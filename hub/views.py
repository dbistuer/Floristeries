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
        price = request.POST['price']
        product = Producte.objects.create(name=name, description=description, price=price)
        return render(request, 'Product/add.html')
    else:
        return render(request, 'Product/add.html')

def newProduct(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        product = Producte.objects.create(name=name,description=description,price=price)
        return render(request, 'Product/add.html')
    else:
        return render(request, 'Product/add.html')