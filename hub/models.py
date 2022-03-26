from typing import Any
from django.core.validators import EmailValidator
from django.db import models
from django.db.models import Model
from .validator import DNIValidator, PhoneValidator, NIFValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CLIENTE = 'CL'
    FLORISTERIA= 'FL'

    TIPOS_USUARIOS = (
        (CLIENTE, 'Cliente'),
        (FLORISTERIA, 'Floristeria'),
    )
    tipo = models.CharField(choices=TIPOS_USUARIOS, max_length=2)
    CP = models.IntegerField()
    ciutat = models.CharField(max_length=50)
    adreca = models.CharField(max_length=200)
    phone = models.CharField(max_length=14, validators=[PhoneValidator])

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

# Create your models here.
class Floristeria(Model):
    NIF = models.CharField(unique=True,max_length=9, validators=[NIFValidator])
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)


class Client(Model):
    DNI = models.CharField(unique=True, validators=[DNIValidator],max_length=9)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

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

