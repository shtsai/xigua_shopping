from django.contrib import admin

from .models import Customer, Order, Product

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
