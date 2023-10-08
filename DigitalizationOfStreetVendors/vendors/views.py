import datetime
import os

from django.contrib.auth.management.commands.changepassword import UserModel
from django.db.models import Q
from django.shortcuts import render, redirect

from vendors.forms import RegistrationForm, LoginForm, ProductForm, ProductRequestForm
from vendors.models import RegistrationModel, ProductModel, TransactionModel,ProductRequestModel

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
#=================================================================================================
import smtplib # simple main transfer protocol -- helps to send mail

def send_mail(email,message):
    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)  # 587 is a port number
        s.starttls()
        s.login("sravyabongu@gmail.com", "bfaxhpriwoqubove")
        print("message:",message)
        s.sendmail("sravyabongu@gmail.com",email,str(message))
        s.quit()

    except Exception as e:
        print("Send OTP via Email","Please enter the valid email address OR check an internet connection")


def registration(request):

    status = False

    if request.method == "POST":
        # Get the posted form
        registrationForm = RegistrationForm(request.POST)

        if registrationForm.is_valid():

            regModel = RegistrationModel()
            regModel.name = registrationForm.cleaned_data["name"]
            regModel.email = registrationForm.cleaned_data["email"]
            regModel.mobile = registrationForm.cleaned_data["mobile"]
            regModel.address = registrationForm.cleaned_data["address"]
            regModel.username = registrationForm.cleaned_data["username"]
            regModel.password = registrationForm.cleaned_data["password"]
            regModel.usertype = registrationForm.cleaned_data["usertype"]
            regModel.status = "no"

            user = RegistrationModel.objects.filter(username=regModel.username).first()

            if user is not None:
                status = False
            else:
                try:
                    regModel.save()
                    status = True
                except Exception as e:
                    print(e)
                    status = False
    if status:
        return render(request, 'login.html', locals())
    else:
        response = render(request, 'registration.html', {"message": "User All Ready Exist"})

    return response

def login(request):

    if request.method == "GET":

        loginForm = LoginForm(request.GET)

        if loginForm.is_valid():

            uname = loginForm.cleaned_data["username"]
            upass = loginForm.cleaned_data["password"]

            if uname == "admin" and upass == "Admin123":

                request.session['username'] = "admin"
                request.session['role'] = "admin"

                return render(request, "users.html", {"users":RegistrationModel.objects.all()})

            else:

                user = RegistrationModel.objects.filter(username=uname, password=upass).first()

                if user is not None:

                    if user.status == "yes":

                        request.session['username'] = uname
                        request.session['role'] = user.usertype
                        request.session['products']=[]

                        if user.usertype=="vendor":
                            return render(request, "products.html",{"products":ProductModel.objects.filter(vendor=uname)})
                        elif user.usertype=="customer":
                            return render(request, "products.html",{"products":ProductModel.objects.all()})
                        elif user.usertype=="distributor":
                            return render(request, "transactions.html",
                                          {"transactions": TransactionModel.objects.filter(
                                              distributor=request.session['username'])})
                        else:
                            del request.session['username']
                            del request.session['role']
                            del request.session['products']
                            return render(request, 'index.html', {"message": "in valid account"})
                    else:
                        return render(request, 'index.html', {"message": "Your Account is not yet Activated"})
                else:
                    return render(request, 'index.html', {"message": "Invalid Credentials"})
        else:
            return render(request, 'index.html', {"message": "Invalid Form"})

    else:
        return render(request, 'index.html', {"message": "Invalid Request"})

def logout(request):
    try:
        del request.session['username']
        del request.session['role']
        del request.session['products']
    except:
        pass
    return render(request, 'index.html', {})

def activateaccount(request):
    RegistrationModel.objects.filter(username=request.GET['username']).update(status=request.GET['status'])
    return render(request, "users.html", {"users":RegistrationModel.objects.all()})

def viewusers(request):
    return render(request, "users.html", {"users":RegistrationModel.objects.all()})

def searchvendor(request):
    return render(request, "users.html", {"users":RegistrationModel.objects.filter(address__contains=request.GET['query'])})

def deleteuser(request):
    userid= request.GET['userid']
    RegistrationModel.objects.filter(username=userid).delete()
    return render(request, "users.html", {"users":RegistrationModel.objects.all()})

#=====================================================================================================

def postProduct(request):

    status = False

    productForm = ProductForm(request.POST)

    if productForm.is_valid():

        name = productForm.cleaned_data['name']
        price = productForm.cleaned_data['price']
        category = productForm.cleaned_data['category']
        description = productForm.cleaned_data['description']
        availableqty = productForm.cleaned_data['availableqty']
        vendor = RegistrationModel.objects.filter(username=request.session['username']).first()
        location=vendor.address

        new_product = ProductModel(name=name,price=price,vendor=vendor.username,category=category,description=description,availableqty=availableqty,location=location)

        try:
            new_product.save()
            status = True
        except:
            status = False

    if status:
        return render(request, "products.html",{"products": ProductModel.objects.filter(vendor=request.session['username'])})
    else:
        response = render(request, 'addproduct.html', {"message": "Product Uploaded Failed"})

    return response

def getProducts(request):
    role=request.session['role']
    if role == "vendor":
        print("in if:",request.session['username'])
        return render(request, "products.html", {"products": ProductModel.objects.filter(vendor=request.session['username'])})
    elif role == "customer":
        return render(request, "products.html", {"products": ProductModel.objects.all()})

def searchproduct(request):
    return render(request, 'products.html', {'products':ProductModel.objects.filter(location__contains=request.GET['query'])})

def deleteProduct(request):

    product_id= request.GET['product']
    ProductModel.objects.filter(id=product_id).delete()
    return render(request, "products.html",{"products": ProductModel.objects.filter(vendor=request.session['username'])})

def updateProduct(request):
    product_id= request.GET['product']
    product=ProductModel.objects.get(id=product_id)
    return render(request, "updateproduct.html",{"product":product_id,"availableqty":product.availableqty,"price":product.price})

def updateProductAction(request):
    product_id= request.GET['product']
    price = request.GET['price']
    availableqty = request.GET['availableqty']
    ProductModel.objects.filter(id=product_id).update(price=price,availableqty=availableqty)
    return render(request, "products.html",{"products": ProductModel.objects.filter(vendor=request.session['username'])})

def buyProduct(request):
    return render(request, 'addtocart.html', {'product':request.GET['product']})

def addtocart(request):

    # get choice list from your session
    product_list = request.session.get('products', [])
    product_list.insert(len(product_list), request.GET['product'] + "_" + request.GET['qty'])
    request.session['products'] = product_list
    print("after add", request.session['products'])

    return render(request, "products.html", {"products": ProductModel.objects.all()})

def viewcart(request):

    products=request.session.get('products', [])

    cart=[]

    for p in products:
        plist=p.split("_")
        product = ProductModel.objects.get(id=plist[0])
        product.cqty = plist[1]
        product.cprice = (int(product.price) / int(product.availableqty)) * int(plist[1])
        cart.append(product)

    return render(request, 'viewcart.html', {'products':cart})

def deletecart(request):
    product_list = request.session.get('products', [])
    product_list.remove(request.GET['product'])
    request.session['products'] = product_list
    print("after removed", request.session['products'])
    return redirect(viewcart)

def submitcart(request):

    request.session['modeofpayment']=request.GET['modeofpayment']

    if request.session['modeofpayment']=="cash on delivery":
        return redirect(buyProductAction)

    elif request.session['modeofpayment']=="online payment":

        products = request.session.get('products', [])
        price=0

        for p in products:
            plist = p.split("_")
            product = ProductModel.objects.get(id=plist[0])
            product.cqty = plist[1]
            price = price+(int(product.price) / int(product.availableqty)) * int(plist[1])

        return render(request, 'payment.html',
                      {'price':price})

def buyProductAction(request):

    customer = RegistrationModel.objects.filter(username=request.session['username']).first()

    products = request.session.get('products', [])

    for p in products:

        plist = p.split("_")

        product = ProductModel.objects.get(id=plist[0])

        vendor=RegistrationModel.objects.filter(username=product.vendor).first()

        transaction = TransactionModel()
        transaction.customerid = request.session['username']
        transaction.productid = plist[0]
        transaction.tdate = datetime.datetime.now()
        transaction.qty = plist[1]
        transaction.modeofpayment = request.session['modeofpayment']
        transaction.distributor =""
        transaction.deliverystatus = ""
        transaction.productname=product.name

        if request.session['modeofpayment'] == "cash on delivery":
            transaction.paymentstatus = "pending"

        elif request.session['modeofpayment'] == "online payment":
            transaction.paymentstatus = "done"

        transaction.vendorlocation = vendor.address
        transaction.customerlocation =customer.address
        transaction.vendorid = product.vendor
        transaction.txamount = (int(product.price) / int(product.availableqty)) * int(plist[1])

        transaction.save()

        send_mail(customer.email,"Your order successfully placed")

    request.session['products']=[]

    return redirect(viewtransactions)

# =======================================================================================================================

def addproductrequest(request):
    vendorid = request.GET['vendorid']
    return render(request, "addproductrequest.html",{"vendorid":vendorid})

def addproductrequestaction(request):

    status = False

    productrequestForm = ProductRequestForm(request.POST)

    if productrequestForm.is_valid():

        print("in if")
        vendor = productrequestForm.cleaned_data['vendorid']
        productname = productrequestForm.cleaned_data['productname']
        qty = productrequestForm.cleaned_data['qty']
        category = productrequestForm.cleaned_data['category']
        description = productrequestForm.cleaned_data['description']

        productrequest = ProductRequestModel(productname=productname,qty=qty, vendorid=vendor, category=category,
                                                 description=description,customerid=request.session['username'],status="pending")
        try:
            productrequest.save()
            status = True
        except:
            status = False

    else:
        print("in else")

    if status:
        return render(request, "viewproductrequests.html", {"productrequests":ProductRequestModel.objects.filter(customerid=request.session['username'])})
    else:
        response = render(request, 'addproductrequest.html', {"message": "Product Request Uploaded Failed"})

    return response

def viewproductrequests(request):

    role = request.session['role']
    if role == "vendor":
        return render(request, "viewproductrequests.html", {"productrequests":ProductRequestModel.objects.filter(vendorid=request.session['username'])})
    elif role == "customer":
        return render(request, "viewproductrequests.html", {"productrequests":ProductRequestModel.objects.filter(customerid=request.session['username'])})

def updateproductrequest(request):
    ProductRequestModel.objects.filter(id=request.GET['id']).update(status=request.GET['status'])
    return render(request, "viewproductrequests.html", {"productrequests":ProductRequestModel.objects.filter(vendorid=request.session['username'])})

def deleteproductrequest(request):

    id=request.GET['id']

    ProductRequestModel.objects.get(id=id).delete()

    role = request.session['role']

    if role == "vendor":
        return render(request, "viewproductrequests.html",
                      {"productrequests": ProductRequestModel.objects.filter(vendorid=request.session['username'])})
    elif role == "customer":
        return render(request, "viewproductrequests.html",
                      {"productrequests": ProductRequestModel.objects.filter(customerid=request.session['username'])})

#=================================================================================================
def viewtransactions(request):

    role = request.session['role']

    if role == "vendor":
        return render(request, "transactions.html",
                      {"transactions": TransactionModel.objects.filter(vendorid=request.session['username'])})
    elif role == "customer":
        return render(request, "transactions.html",
                      {"transactions": TransactionModel.objects.filter(customerid=request.session['username'])})
    elif role == "distributor":
        return render(request, "transactions.html",
                      {"transactions": TransactionModel.objects.filter(distributor=request.session['username'])})

def vieworders(request):
    return render(request, "orders.html",
                      {"transactions": TransactionModel.objects.filter(distributor="")})

def searchtransaction(request):
    query=request.GET['query']
    return render(request, "transactions.html", {"transactions":TransactionModel.objects.filter(Q(customerlocation__icontains=query) | Q(vendorlocation__icontains=query))})

def acceptdelivery(request):
    TransactionModel.objects.filter(id=request.GET['id']).update(distributor=request.session['username'])
    return render(request, "orders.html",
                  {"transactions": TransactionModel.objects.filter(distributor="")})

def updatetransactionstatus(request):
    product_id= request.GET['id']
    return render(request, "updatetransaction.html",{"product":product_id})

def updatetransactionstatusaction(request):

    statustype=request.GET['statustype']

    if statustype=="delivery":
        TransactionModel.objects.filter(id=request.GET['id']).update(deliverystatus=request.GET['status'])
    elif statustype=="payment":
        TransactionModel.objects.filter(id=request.GET['id']).update(paymentstatus=request.GET['status'])

    return render(request, "transactions.html",
                  {"transactions": TransactionModel.objects.filter(distributor=request.session['username'])})