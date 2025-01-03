from django.contrib import admin

from customers.models import Customer
from django.contrib.auth.admin import UserAdmin
from .models import Customer

admin.site.register(Customer, UserAdmin)
admin.site.register(Customer)