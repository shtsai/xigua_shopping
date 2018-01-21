from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db import connection
from django.contrib.auth.decorators import login_required
from backend.models import Customer, Order, Product, Inventory


class CustomerView(generic.ListView):
    template_name = 'backend/customer.html'
    context_object_name = 'customer_list'

    def get_queryset(self):
        return Customer.objects.raw('SELECT * FROM backend_customer ORDER BY cid')
