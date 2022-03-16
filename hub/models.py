from typing import Any

from django.core.validators import EmailValidator
from django.db import models
from django.db.models import Model
from .validator import DNIValidator, PhoneValidator, IBANValidator, NIFValidator

# Create your models here.
class Floristeria(Model):
    nom = models.CharField(max_length=100)
    NIF = models.CharField(unique=True,max_length=9, validators=[NIFValidator])
    CP = models.IntegerField()
    Ciutat = models.CharField(max_length=50)
    Adreca = models.CharField(max_length=200)
    email = models.CharField(max_length=70,validators=[EmailValidator])
    phone = models.CharField(max_length=14,validators=[PhoneValidator])

class Producte(Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    price = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return self.name


class Client(Model):
    nom = models.CharField(max_length=100)
    DNI = models.CharField(unique=True, validators=[DNIValidator],max_length=9)
    CP = models.CharField(max_length=5)
    Ciutat = models.CharField(max_length=70)
    Aderca = models.CharField(max_length=200)
    IBAN = models.CharField(validators=[IBANValidator], max_length=20)
    email = models.CharField(max_length=70, validators=[EmailValidator])
    phone = models.CharField(max_length=14, validators=[PhoneValidator])

class Compra(Model):
    idFloristeria = models.IntegerField()
    idClient = models.IntegerField()
    data = models.DateTimeField()

    class Meta:
        unique_together = (("idFloristeria","idClient"),)

class Elements(Model):
    idCompra = models.IntegerField()
    idProducte = models.IntegerField()
    cantitat = models.IntegerField()

    class Meta:
        unique_together = (("idCompra","idProducte"),)

class Stock(Model):
    idFloristeria = models.IntegerField()
    idProducte = models.IntegerField()
    cantitat = models.IntegerField()

    class Meta:
        unique_together = (("idFloristeria","idProducte"),)

