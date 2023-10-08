from django.contrib import admin
from vendors.models import RegistrationModel,ProductModel,ProductRequestModel,TransactionModel

admin.site.register(RegistrationModel)
admin.site.register(ProductModel)
admin.site.register(ProductRequestModel)
admin.site.register(TransactionModel)