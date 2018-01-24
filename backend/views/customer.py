from django.shortcuts import render, get_object_or_404, redirect
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

def addcustomer(request):
    customer = Customer.create(request.POST['name'])
    if (request.POST['address'] != ""):
        customer.caddr = request.POST['address'] 
    if (request.POST['phone'] != ""):
        customer.cphone = request.POST['phone'] 
    if (request.POST['wechat'] != ""):
        customer.cwechat = request.POST['wechat'] 
    if (request.POST['note'] != ""):
        customer.cnote = request.POST['note'] 
    customer.save()
    return redirect("/customer/" + str(customer.cid))
