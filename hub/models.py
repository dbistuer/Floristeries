from typing import Any
from django.core.validators import EmailValidator
from django.db import models
from django.db.models import Model
from .validator import DNIValidator, PhoneValidator, NIFValidator
from django.contrib.auth.models import User


# Create your models here.
class Floristeria(Model):
    nom = models.CharField(max_length=100)
    NIF = models.CharField(unique=True,max_length=9, validators=[NIFValidator])
    CP = models.IntegerField()
    Ciutat = models.CharField(max_length=50)
    Adreca = models.CharField(max_length=200)
    email = models.CharField(max_length=70,validators=[EmailValidator])
    phone = models.CharField(max_length=14,validators=[PhoneValidator])
    User = models.OneToOneField(User,on_delete=models.DO_NOTHING)


class Client(Model):
    nom = models.CharField(max_length=100)
    DNI = models.CharField(unique=True, validators=[DNIValidator],max_length=9)
    CP = models.CharField(max_length=5)
    Ciutat = models.CharField(max_length=70)
    Aderca = models.CharField(max_length=200)
    email = models.CharField(max_length=70, validators=[EmailValidator])
    phone = models.CharField(max_length=14, validators=[PhoneValidator])
    User = models.OneToOneField(User, on_delete=models.DO_NOTHING)

class Producte(Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    price = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return self.name

class Compra(Model):
    Floristeria = models.ForeignKey(Floristeria,on_delete=models.DO_NOTHING)
    Client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    data = models.DateTimeField()

    class Meta:
        unique_together = (("Floristeria","Client"),)

class Elements(Model):
    Compra = models.ForeignKey(Compra,on_delete=models.DO_NOTHING)
    Producte = models.ForeignKey(Producte,on_delete=models.DO_NOTHING)
    cantitat = models.IntegerField()

    class Meta:
        unique_together = (("Compra","Producte"),)

class Stock(Model):
    Floristeria = models.ForeignKey(Floristeria,on_delete=models.DO_NOTHING)
    Producte = models.ForeignKey(Producte,on_delete=models.DO_NOTHING)
    cantitat = models.IntegerField()

    class Meta:
        unique_together = (("Floristeria","Producte"),)

