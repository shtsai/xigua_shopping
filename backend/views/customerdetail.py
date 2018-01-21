from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db import connection
from django.contrib.auth.decorators import login_required
from backend.models import Customer, Order, Product, Inventory
from .util import *


def customerdetail(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    template_name = 'backend/customer_detail.html'
#    orders = Order.objects.filter(cid_id=customer.cid);
    orders = get_customer_orders(customer_id)
    return render(request, template_name, {
        'customer': customer,
        'message': "hello cash",
        'orders': orders,
    })

def get_customer_orders(customer_id):
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT *
                        FROM backend_customer AS C JOIN backend_order AS O ON C.cid = O.cid_id
                        WHERE C.cid = %s
                        ''', [customer_id])
        res = dictfetchall(cursor)
        return res
