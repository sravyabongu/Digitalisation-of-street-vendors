from django.forms import Form, CharField, PasswordInput, FileField


class RegistrationForm(Form):

    username =CharField(max_length=50)
    name = CharField(max_length=50)
    password =CharField(max_length=50)
    email =CharField(max_length=50)
    mobile =CharField(max_length=50)
    address =CharField(max_length=50)
    usertype =CharField(max_length=50)

class LoginForm(Form):

    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())

class ProductForm(Form):

    name = CharField(max_length=30)
    price = CharField(max_length=30)
    availableqty = CharField(max_length=30)
    category = CharField(max_length=30)
    description = CharField(max_length=500)

class ProductRequestForm(Form):
    vendorid = CharField(max_length=30)
    category=CharField(max_length=30)
    qty= CharField(max_length=30)
    productname = CharField(max_length=30)
    description= CharField(max_length=30)