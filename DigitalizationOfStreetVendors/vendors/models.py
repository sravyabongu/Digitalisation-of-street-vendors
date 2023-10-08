from django.db import models
from django.db.models import Model

# Create your models here.
class RegistrationModel(Model):

    username=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    usertype = models.CharField(max_length=50)
    status= models.CharField(max_length=50)

    class Meta:
        db_table = "registration model"


class ProductModel(models.Model):

    name = models.CharField(max_length=30)
    price = models.CharField(max_length=30)
    availableqty=models.CharField(max_length=30)
    category=models.CharField(max_length=30)
    vendor=models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    location=models.CharField(max_length=30)

class TransactionModel(models.Model):

    customerid=models.CharField(max_length=100)
    productid=models.CharField(max_length=100)
    productname = models.CharField(max_length=100)
    tdate=models.DateTimeField(auto_now=True, blank=False, null=False)
    qty = models.CharField(max_length=100)
    modeofpayment=models.CharField(max_length=100)
    distributor=models.CharField(max_length=100)
    deliverystatus = models.CharField(max_length=100)
    paymentstatus = models.CharField(max_length=100)
    vendorlocation=models.CharField(max_length=100)
    customerlocation=models.CharField(max_length=100)
    vendorid=models.CharField(max_length=100)
    txamount=models.CharField(max_length=100)

class ProductRequestModel(models.Model):

    customerid= models.CharField(max_length=30)
    vendorid= models.CharField(max_length=30)
    category=models.CharField(max_length=30)
    qty= models.CharField(max_length=30)
    productname = models.CharField(max_length=30)
    description= models.CharField(max_length=30)
    status = models.CharField(max_length=50)