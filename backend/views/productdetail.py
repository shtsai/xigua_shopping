from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db import connection
from django.contrib.auth.decorators import login_required
from backend.models import Customer, Order, Product, Inventory
from .util import *

def productdetail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    template_name = 'backend/product_detail.html'
    return render(request, template_name, {
        'product': product,
    })
    