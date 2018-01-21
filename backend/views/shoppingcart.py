from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db import connection
from django.contrib.auth.decorators import login_required
from backend.models import Customer, Order, Product, Inventory

def addtocart(request, product_id):
    if not (str(product_id) in request.session):
        request.session['cart'][str(product_id)] = 1
    else:
        request.session['cart'][str(product_id)] += 1
    return product(request)

