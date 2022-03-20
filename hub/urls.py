from django.urls import path
from . import views

urlpatterns = [
    #product
    path('product/list',views.listProducts, name='productList'),
    path('product/add',views.addProduct, name='productAdd'),
    path('product/detail/<int:id>',views.detailProduct, name='productDetail'),
    #sdfsdf
    path('compra/show/<int:id>',views.boughtElements, name='productsBought'),
    #path('',views.movieList),
    #path('',views.SignIn)
]
