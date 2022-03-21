from django.urls import path
from . import views

urlpatterns = [
    #product
    path('product/list',views.listProducts, name='productList'),
    path('product/add',views.addProduct, name='productAdd'),
    path('product/detail/<int:id>',views.detailProduct, name='productDetail'),
    #sdfsdf
    path('compra/show/<int:id>',views.boughtElements, name='productsBought'),
    #stock
    path('stock/list',views.listStock, name='stockList'),
    path('stock/add',views.addStock, name='stockAdd'),
    path('stock/edit/<int:id>',views.editStock, name='stockEdit'),
    path('stock/delete/<int:id>',views.deleteStock, name='stockDelete'),
    #path('',views.movieList),
    #path('',views.SignIn)
]
