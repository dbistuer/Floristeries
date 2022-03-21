from django.shortcuts import render, redirect
from .models import *
# Create your views here.
##PRODUCT
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
    json={'product':Producte.objects.get(id=id)}
    return render(request, 'Product/detail.html',json)
###END PRODUCT

def boughtElements(request):
    compra = request.compra
    elements = Elements.objects.get(Compra=compra)
    json={'elements':elements}
    return render(request, 'Compra/show.html')

### STROCK

def listStock(request):
    productes = Stock.objects.all()
    return render(request, "Stock/list.html", {"productes": productes})

def addStock(request):
    if request.method == 'POST':
        idp = request.POST['idProducte']
        producte = Producte.objects.get(pk=idp)
        cantitat = int(request.POST['cantitat'])
        #TODO: Get idFloristeria del usuari que ha de ser de tipus floristeria
        Stock.objects.create(Floristeria=Floristeria.objects.get(pk=1), Producte=producte, cantitat=cantitat)
        return render(request, 'Stock/add.html',{'products':Producte.objects.all()})
    else:
        return render(request, 'Stock/add.html',{'products':Producte.objects.all()})

def editStock(request, id):
    product = Stock.objects.get(id=id)
    json={'product':Producte.objects.get(id=id)}
    return render(request, 'Product/detail.html',json)

### END STOCK