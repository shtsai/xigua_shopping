from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db import connection
from django.contrib.auth.decorators import login_required
from backend.models import Customer, Order, Product, Inventory
from .util import *

def inventorydetail(request, inventory_id):
    inventory = get_object_or_404(Inventory, pk=inventory_id)
    template_name = 'backend/inventory_detail.html'
    items = get_inventory_items(inventory_id)
    return render(request, template_name, {
        'inventory': inventory,
        'items': items,
    })
    
def get_inventory_items(inventory_id):
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT *
                        FROM backend_inventory AS I JOIN backend_inventorycontains AS IC ON I.iid = IC.iid_id JOIN backend_product AS P ON P.pid = IC.pid_id
                        WHERE I.iid = %s
                        ''', [inventory_id])
        res = dictfetchall(cursor)
        return res

