from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db import connection
from django.contrib.auth.decorators import login_required
from backend.models import Customer, Order, Product, Inventory
from .util import *


def order(request):
    order = get_all_orders()
    pendingorder = get_pending_orders()
    paidorder = get_paid_orders()
    shippedorder = get_shipped_orders()
    completedorder = get_completed_orders()
    template_name = 'backend/order.html'
    return render(request, template_name, {
        'order': order,    
        'pendingorder': pendingorder,
        'paidorder': paidorder,
        'shippedorder': shippedorder,
        'completedorder': completedorder,
    }) 

def get_all_orders():
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT *
                        FROM backend_order AS O JOIN backend_customer AS C ON O.cid_id = C.cid
                        ORDER BY O.odate DESC 
                        ''')
        res = dictfetchall(cursor)
        return res

def get_pending_orders():
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT *
                        FROM backend_order AS O JOIN backend_customer AS C ON O.cid_id = C.cid
                        WHERE ostatus="pending"
                        ORDER BY O.odate DESC 
                        ''')
        res = dictfetchall(cursor)
        return res

def get_paid_orders():
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT *
                        FROM backend_order AS O JOIN backend_customer AS C ON O.cid_id = C.cid
                        WHERE ostatus="paid"
                        ORDER BY O.odate DESC 
                        ''')
        res = dictfetchall(cursor)
        return res

def get_shipped_orders():
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT *
                        FROM backend_order AS O JOIN backend_customer AS C ON O.cid_id = C.cid
                        WHERE ostatus="shipped"
                        ORDER BY O.odate DESC 
                        ''')
        res = dictfetchall(cursor)
        return res
    
def get_completed_orders():
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT *
                        FROM backend_order AS O JOIN backend_customer AS C ON O.cid_id = C.cid
                        WHERE ostatus="completed"
                        ORDER BY O.odate DESC 
                        ''')
        res = dictfetchall(cursor)
        return res
