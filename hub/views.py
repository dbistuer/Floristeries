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

def addProduct(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = float(request.POST['price'].replace(",","."))
        Producte.objects.create(name=name, description=description, price=price)
        return render(request, 'Product/add.html')
    else:
        return render(request, 'Product/add.html')

def detailProduct(request, id):
    product = Producte.objects.get(id=id)
    json={'product':Producte.objects.get(id=id)}
    return render(request, 'Product/detail.html',json)
###END PRODUCT

def boughtElements(request):
    if request.user.is_authenticated:
        compra = request.compra
        elements = Elements.objects.get(Compra=compra)
        json={'elements':elements}
        return render(request, 'Compra/show.html')
    else:
        return render(request,"Compra/compra_not_authenticated.html")
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
    if request.method == "POST":
        product.cantitat = int(request.POST['cantitat'])
        product.save()
    json = {'product': product}
    return render(request, 'Stock/edit.html', json)


def deleteStock(request, id):
    stock = Stock.objects.get(pk=id)
    stock.delete()
    productes = Stock.objects.all()
    return render(request, "Stock/list.html", {"productes": productes})


### END STOCK

def SignIn(request):
    if request.method == 'GET':
        return render(request, 'Registration/signin.html')

    if request.method == 'POST':
        name = request.POST['name']
        second_name = request.POST['second_name']
        last_name = request.POST['last_name']
        DNI = request.POST['DNI']
        ciutat = request.POST['ciutat']
        CP = request.POST['CP']
        adress = request.POST['adress']
        phone = request.POST['phone']
        email = request.POST['email']
        alias = request.POST['alias']
        password = request.POST['password']
        tipo = request.POST['tipo']

        # Validate input data
        if not (name and DNI and adress and phone and email and alias and password):
            # Missing values
            return render(request, 'Registration/MissingValues.html')

        error = validate_data(DNI,phone)
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
        client = Client(user=user, DNI=DNI)
        client.save()
        return redirect('login')

def validate_data(DNI='', phoneNumber=''):
    error = ''
    if DNI:
        try:
            DNIValidator(DNI)
        except:
            error += 'DNI is not valid.'
    if phoneNumber:
        try:
            PhoneValidator(phoneNumber)
        except:
            error += 'Phone number is not valid.   '
    return error

@login_required
def profile(request):
    user=request.user
    client = Client.objects.get(user=user)
    json = {'client': client}
    return render(request, 'User/profile.html', json)


@login_required
def edit_profile(request):
    user = request.user
    client = Client.objects.get(user=user)
    if request.method == 'GET':
        json = {'client': client }
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
