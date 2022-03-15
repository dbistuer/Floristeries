from django.contrib import admin
from hub.models import Floristeria, Compra, Producte, Client, Elements, Stock

# Register your models here.
admin.site.register(Floristeria)
admin.site.register(Client)
admin.site.register(Compra)
admin.site.register(Producte)
admin.site.register(Elements)
admin.site.register(Stock)