from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from .validator import *
# Create your views here.
##PRODUCT

def home(request):
    return render(request,'Floristeria/home.html')

def listProducts(request):
    productes = Producte.objects.all()
    return render(request, "Product/list.html", {"productes": productes})

@login_required
def addProduct(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        Producte.objects.create(name=name, description=description)
        return render(request, 'Product/add.html')
    else:
        return render(request, 'Product/add.html')

def detailProduct(request, id):
    producte = Producte.objects.filter(id=id)
    stocks = Stock.objects.filter(producte_id=producte[0].id).order_by('price')
    json={'stocks':stocks}
    return render(request, 'Product/detail.html',json)

@login_required
def buyProduct(request):
    pid = request.POST['id']
    fid = request.POST['idFlor']
    cantitat = int(request.POST['cantitat'])
    floristeria = Floristeria.objects.get(id=fid)
    producte = Producte.objects.get(id=pid)
    stock = Stock.objects.filter(floristeria=floristeria, producte=producte)
    if cantitat <= stock[0].cantitat:
        client = Client.objects.get(user=request.user)
        compra = Compra.objects.create(floristeria=floristeria,client=client,data=datetime.now())
        compra.save()
        element = Elements.objects.create(compra=compra,producte=producte,cantitat=cantitat,price=stock[0].price)
        element.save()
        stock[0].cantitat = stock[0].cantitat - cantitat
        stock.update()
    else:
        error += 'Not valid amount.'
    return render(request,'Floristeria/home.html')
###END PRODUCT
@login_required
def boughtElements(request):
    if request.user.is_authenticated:
        client = Client.objects.get(user=request.user)
        compra = Compra.objects.filter(client=client)
        elements = Elements.objects.filter(compra__in=compra)
        json={'elements':elements}
        return render(request, 'Compra/show.html',json)
    else:
        return render(request,"Compra/compra_not_authenticated.html")
### STROCK

@login_required
def listStock(request):
    productes = Stock.objects.filter(floristeria=request.user.floristeria)
    return render(request, "Stock/list.html", {"productes": productes})

@login_required
def addStock(request):
    if request.method == 'POST':
        idp = request.POST['idProducte']
        producte = Producte.objects.get(pk=idp)
        cantitat = int(request.POST['cantitat'])
        preu = float(str(request.POST['price']).replace(',','.'))
        Stock.objects.create(floristeria=request.user.floristeria, producte=producte, cantitat=cantitat,price=preu)
        return render(request, 'Stock/add.html',{'products':Producte.objects.all()})
    else:
        return render(request, 'Stock/add.html',{'products':Producte.objects.all()})

@login_required
def editStock(request, id):
    stock = Stock.objects.get(id=id)
    if request.method == "POST":
        stock.cantitat = int(request.POST['cantitat'])
        stock.price = float(str(request.POST['price']).replace(',','.'))
        stock.save()
    json = {'product': stock}
    return render(request, 'Stock/edit.html', json)

@login_required
def deleteStock(request, id):
    stock = Stock.objects.get(pk=id)
    stock.delete()
    productes = Stock.objects.all()
    return render(request, "Stock/list.html", {"productes": productes})

### END STOCK

def SignIn(request,tipo):
    tipo = str(tipo)[1:len(str(tipo))]
    if request.method == 'GET':
        if tipo == User.CLIENTE or tipo == User.FLORISTERIA:
            json = {'tipo':tipo}
            return render(request, 'Registration/signin.html',json)
        else:
            return render(request, '/')

    if request.method == 'POST':
        name = request.POST['name']
        second_name = request.POST['second_name']
        last_name = request.POST['last_name']
        if tipo == User.CLIENTE:
            DNI = request.POST['DNI']
        elif tipo == User.FLORISTERIA:
            NIF = request.POST['NIF']
        else:
            return render(request, '/')
        ciutat = request.POST['ciutat']
        CP = request.POST['CP']
        adress = request.POST['adress']
        phone = request.POST['phone']
        email = request.POST['email']
        alias = request.POST['alias']
        password = request.POST['password']


        # Validate input data
        if tipo == User.CLIENTE:
            if not (name and DNI and adress and phone and email and alias and password):
                return render(request, 'Registration/MissingValues.html')
            error = validate_data(DNI=DNI, phone=phone,tipo=tipo)
        else:
            if not (name and NIF and adress and phone and email and alias and password):
                return render(request, 'Registration/MissingValues.html')
            error = validate_data(phone=phone, NIF=NIF,tipo=tipo)

        if error:
            json = {'error': error, 'register': True}
            return render(request, 'Registration/InvalidValues.html', json)

        if User.objects.filter(username=alias).exists():
            json = {'error': 'Username already exist, you will have to choose another one.', 'register': True}
            return render(request, 'Registration/InvalidValues.html', json)

        user = User(username=alias, email=email,  password=password,
                    first_name=name,last_name=second_name+' '+last_name,
                    phone=phone, adreca=adress, CP=CP, ciutat=ciutat, tipo=tipo)
        user.set_password(password)
        user.save()
        if tipo == User.CLIENTE:
            client = Client(user=user, DNI=DNI)
            client.save()
        else:
            floristeria = Floristeria(user=user, NIF=NIF)
            floristeria.save()
        return redirect('login')

def validate_data(DNI='', phone='',NIF='',tipo=''):
    error = ''
    if tipo == 'CL':
        if DNI:
            try:
                DNIValidator(DNI)
            except:
                error += 'DNI is not valid.'
    else:
        if NIF:
            try:
                NIFValidator(NIF)
            except:
                error += 'NIF is not valid.'
    if phone:
        try:
            PhoneValidator(phone)
        except:
            error += 'Phone number is not valid.   '
    return error

@login_required
def profile(request):
    user=request.user
    if user.tipo == User.CLIENTE:
        entity = Client.objects.get(user=user)
    else:
        entity = Floristeria.objects.get(user=user)
    json = {'entity': entity}
    return render(request, 'User/profile.html', json)

@login_required
def edit_profile(request):
    user = request.user
    if user.tipo == User.CLIENTE:
        entity = Client.objects.get(user=user)
    else:
        entity = Floristeria.objects.get(user=user)
    if request.method == 'GET':
        json = {'entity': entity }
        return render(request, 'User/ModifyProfile.html', json)
    elif request.method == 'POST':
        first_name = request.POST['first_name']
        nameSplitted = request.POST['last_name'].split()
        second_name = nameSplitted[0]
        last_name = nameSplitted[1]
        DNI = request.POST['DNI']
        adreca = request.POST['adreca']
        CP = request.POST['CP']
        ciutat = request.POST['ciutat']
        phone = request.POST['phone']
        email = request.POST['email']
        alias = request.POST['alias']
        cardNumber = request.POST['cardNumber']

        error = validate_data(DNI, phone)
        if error:
            json = {'error': error, 'register': False}
            return render(request, 'registration/InvalidValues.html', json)

        if alias:
            if User.objects.filter(username=alias).exists() and not user.username == alias:
                json = {'error': 'Username already exist, you will have to choose another one.', 'register': False}
                return render(request, 'registration/InvalidValues.html', json)
            user.username = alias
        if first_name and user.first_name != first_name:
            user.first_name = first_name
        if email and user.email != email:
            user.email = email
        if phone and user.phone != phone:
            user.phone = phone
        if adreca and user.adreca != adreca:
            user.adreca = adreca
        user.save()

        if DNI and client.DNI != DNI:
            client.DNI = DNI
        if cardNumber:
            client.cardNumber = cardNumber
        client.save()
        return redirect('profile')

