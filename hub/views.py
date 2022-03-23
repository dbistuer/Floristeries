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
        DNI = request.POST['DNI']
        address = request.POST['address']
        phoneNumber = request.POST['phoneNumber']
        email = request.POST['email']
        alias = request.POST['alias']
        password = request.POST['password']
        cardNumber = request.POST['cardNumber']

        # Validate input data
        if not (name and DNI and address and phoneNumber and email and alias and password and cardNumber):
            # Missing values
            return render(request, 'Registration/MissingValues.html')

        error = validate_data(DNI, cardNumber, phoneNumber)
        if error:
            json = {'error': error, 'register': True}
            return render(request, 'Registration/InvalidValues.html', json)

        if User.objects.filter(username=alias).exists():
            json = {'error': 'Username already exist, you will have to choose another one.', 'register': True}
            return render(request, 'Registration/InvalidValues.html', json)

        user = User(username=alias, email=email, first_name=name)
        user.set_password(password)
        user.save()

        client = Client.objects.get(user=user)
        client.address = address
        client.DNI = DNI
        client.cardNumber = cardNumber
        client.telephone = phoneNumber
        client.save()
        return redirect('login')

def validate_data(DNI='', cardNumber='', phoneNumber=''):
    error = ''
    if DNI:
        try:
            DNIValidator(DNI)
        except:
            error += 'DNI is not valid.'
    if cardNumber:
        try:
            IBANValidator(cardNumber)
        except:
            error += 'IBAN is not valid.   '
    if phoneNumber:
        try:
            PhoneValidator(phoneNumber)
        except:
            error += 'Phone number is not valid.   '
    return error

def SignIn(request):
    if request.method == 'GET':
        return render(request, 'Registration/signin.html')

    if request.method == 'POST':
        name = request.POST['name']
        DNI = request.POST['DNI']
        address = request.POST['address']
        phoneNumber = request.POST['phoneNumber']
        email = request.POST['email']
        alias = request.POST['alias']
        password = request.POST['password']
        cardNumber = request.POST['cardNumber']

        # Validate input data
        if not (name and DNI and address and phoneNumber and email and alias and password and cardNumber):
            # Missing values
            return render(request, 'Registration/MissingValues.html')

        error = validate_data(DNI, cardNumber, phoneNumber)
        if error:
            json = {'error': error, 'register': True}
            return render(request, 'Registration/InvalidValues.html', json)

        if User.objects.filter(username=alias).exists():
            json = {'error': 'Username already exist, you will have to choose another one.', 'register': True}
            return render(request, 'Registration/InvalidValues.html', json)

        user = User(username=alias, email=email, first_name=name)
        user.set_password(password)
        user.save()

        client = Client.objects.get(user=user)
        client.address = address
        client.DNI = DNI
        client.cardNumber = cardNumber
        client.telephone = phoneNumber
        client.save()
        return redirect('login')

def validate_data(DNI='', cardNumber='', phoneNumber=''):
    error = ''
    if DNI:
        try:
            DNIValidator(DNI)
        except:
            error += 'DNI is not valid.'
    if cardNumber:
        try:
            IBANValidator(cardNumber)
        except:
            error += 'IBAN is not valid.   '
    if phoneNumber:
        try:
            PhoneValidator(phoneNumber)
        except:
            error += 'Phone number is not valid.   '
    return error

def SignIn(request):
    if request.method == 'GET':
        return render(request, 'Registration/signin.html')

    if request.method == 'POST':
        name = request.POST['name']
        DNI = request.POST['DNI']
        address = request.POST['address']
        phoneNumber = request.POST['phoneNumber']
        email = request.POST['email']
        alias = request.POST['alias']
        password = request.POST['password']
        cardNumber = request.POST['cardNumber']

        # Validate input data
        if not (name and DNI and address and phoneNumber and email and alias and password and cardNumber):
            # Missing values
            return render(request, 'Registration/MissingValues.html')

        error = validate_data(DNI, cardNumber, phoneNumber)
        if error:
            json = {'error': error, 'register': True}
            return render(request, 'Registration/InvalidValues.html', json)

        if User.objects.filter(username=alias).exists():
            json = {'error': 'Username already exist, you will have to choose another one.', 'register': True}
            return render(request, 'Registration/InvalidValues.html', json)

        user = User(username=alias, email=email, first_name=name)
        user.set_password(password)
        user.save()

        client = Client.objects.get(user=user)
        client.address = address
        client.DNI = DNI
        client.cardNumber = cardNumber
        client.telephone = phoneNumber
        client.save()
        return redirect('login')

def validate_data(DNI='', cardNumber='', phoneNumber=''):
    error = ''
    if DNI:
        try:
            DNIValidator(DNI)
        except:
            error += 'DNI is not valid.'
    if cardNumber:
        try:
            IBANValidator(cardNumber)
        except:
            error += 'IBAN is not valid.   '
    if phoneNumber:
        try:
            PhoneValidator(phoneNumber)
        except:
            error += 'Phone number is not valid.   '
    return error

def SignIn(request):
    if request.method == 'GET':
        return render(request, 'Registration/signin.html')

    if request.method == 'POST':
        name = request.POST['name']
        DNI = request.POST['DNI']
        address = request.POST['address']
        phoneNumber = request.POST['phoneNumber']
        email = request.POST['email']
        alias = request.POST['alias']
        password = request.POST['password']
        cardNumber = request.POST['cardNumber']

        # Validate input data
        if not (name and DNI and address and phoneNumber and email and alias and password and cardNumber):
            # Missing values
            return render(request, 'Registration/MissingValues.html')

        error = validate_data(DNI, cardNumber, phoneNumber)
        if error:
            json = {'error': error, 'register': True}
            return render(request, 'Registration/InvalidValues.html', json)

        if User.objects.filter(username=alias).exists():
            json = {'error': 'Username already exist, you will have to choose another one.', 'register': True}
            return render(request, 'Registration/InvalidValues.html', json)

        user = User(username=alias, email=email, first_name=name)
        user.set_password(password)
        user.save()

        client = Client.objects.get(user=user)
        client.address = address
        client.DNI = DNI
        client.cardNumber = cardNumber
        client.telephone = phoneNumber
        client.save()
        return redirect('login')

def validate_data(DNI='', cardNumber='', phoneNumber=''):
    error = ''
    if DNI:
        try:
            DNIValidator(DNI)
        except:
            error += 'DNI is not valid.'
    if cardNumber:
        try:
            IBANValidator(cardNumber)
        except:
            error += 'IBAN is not valid.   '
    if phoneNumber:
        try:
            PhoneValidator(phoneNumber)
        except:
            error += 'Phone number is not valid.   '
    return error

def SignIn(request):
    if request.method == 'GET':
        return render(request, 'Registration/signin.html')

    if request.method == 'POST':
        name = request.POST['name']
        DNI = request.POST['DNI']
        address = request.POST['address']
        phoneNumber = request.POST['phoneNumber']
        email = request.POST['email']
        alias = request.POST['alias']
        password = request.POST['password']

        # Validate input data
        if not (name and DNI and address and phoneNumber and email and alias and password):
            # Missing values
            return render(request, 'Registration/MissingValues.html')

        error = validate_data(DNI,phoneNumber)
        if error:
            json = {'error': error, 'register': True}
            return render(request, 'Registration/InvalidValues.html', json)

        if User.objects.filter(username=alias).exists():
            json = {'error': 'Username already exist, you will have to choose another one.', 'register': True}
            return render(request, 'Registration/InvalidValues.html', json)

        user = User(username=alias, email=email, first_name=name)
        user.set_password(password)
        user.save()

        client = Client.objects.get(user=user)
        client.address = address
        client.DNI = DNI
        client.telephone = phoneNumber
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
