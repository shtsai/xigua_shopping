from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db import connection
from django.contrib.auth.decorators import login_required
from backend.models import Customer, Order, Product, Inventory

def inventory(request):
    inventory = Inventory.objects.all()
    template_name = 'backend/inventory.html'
    return render(request, template_name, {
        'inventory': inventory,
    })
