"""
URL configuration for EPlasticManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.views.generic import TemplateView
from vendors.views import login, registration, logout, postProduct, getProducts, deleteProduct, buyProduct, \
    buyProductAction, deleteuser, viewusers, activateaccount, addproductrequest, viewproductrequests, \
    addproductrequestaction, deleteproductrequest, updateproductrequest, viewtransactions, updateProduct, \
    updateProductAction, acceptdelivery, updatetransactionstatusaction, updatetransactionstatus, addtocart, viewcart, \
    deletecart, submitcart, vieworders, searchvendor

urlpatterns = [

    path('admin/', admin.site.urls),

    path('',TemplateView.as_view(template_name = 'index.html'),name='login'),
    path('login/',TemplateView.as_view(template_name = 'login.html'),name='login'),
    path('loginaction/',login,name='loginaction'),

    path('registration/',TemplateView.as_view(template_name = 'registration.html'),name='registration'),
    path('regaction/',registration,name='regaction'),
    path('viewusers/',viewusers,name='regaction'),
    path('activateaccount/',activateaccount,name='regaction'),
    path('deleteuser/',deleteuser,name='deleteproducts'),

    path('addproductrequest/',addproductrequest,name='postproduct'),
    path('addproductrequestaction/',addproductrequestaction,name='postproductaction'),
    path('viewproductrequests/',viewproductrequests,name='productlist'),
    path('updateproductrequest/',updateproductrequest,name='productlist'),
    path('deleteproductrequest/',deleteproductrequest,name='productlist'),

    path('addproduct/',TemplateView.as_view(template_name = 'addproduct.html'),name='postproduct'),
    path('addproductaction/',postProduct,name='postproductaction'),
    path('viewproducts/',getProducts,name='productlist'),
    path('deleteproduct/',deleteProduct,name='deleteproducts'),
    path('updateproduct/',updateProduct,name='deleteproducts'),
    path('updateproductaction/',updateProductAction,name='deleteproducts'),
    path('searchvendor/',searchvendor,name='deleteproducts'),

    path('buyproduct/',buyProduct,name='buyproduct'),
    path('addtocartaction/',addtocart,name='deleteproducts'),
    path('viewcart/',viewcart,name='deleteproducts'),
    path('deletecart/',deletecart,name='deleteproducts'),
    path('submitcart/',submitcart,name='deleteproducts'),
    path('buyproduct/',buyProduct,name='buyproduct'),
    path('buyproductaction/',buyProductAction,name='buyproductaction'),

    path('viewtransactions/',viewtransactions,name='postproduct'),
    path('vieworders/',vieworders,name='postproduct'),
    path('acceptdelivery/',acceptdelivery,name='deleteproducts'),

    path('updatetransaction/',updatetransactionstatus,name='deleteproducts'),
    path('updatetransactionstatusaction/',updatetransactionstatusaction,name='deleteproducts'),

    path('logout/', logout, name='logout'),
]
