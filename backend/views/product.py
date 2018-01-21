from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db import connection
from django.contrib.auth.decorators import login_required
from backend.models import Customer, Order, Product, Inventory
from .util import *


def product(request):
    foodproduct = get_food_products()
    healthproduct = Product.objects.filter(ptype="Health")
    template_name = 'backend/product.html'
    if not ('cart' in request.session):
        request.session['cart'] = {}
    cart = request.session['cart']
    return render(request, template_name, {
        'foodproduct': foodproduct,
        'healthproduct': healthproduct,
        'cart': cart,
    })

def get_food_products():
    with connection.cursor() as cursor:
        cursor.execute('''
                       SELECT PIN.pid, pname, PIN.ptype, pcost, pprice, PIN.sin AS sin, POUT.sout AS sout, (PIN.sin - POUT.sout) AS soh
                       FROM 
                            (SELECT pid, pname, ptype, pcost, pprice, SUM(iquantity) AS sin 
                            FROM backend_product P LEFT OUTER JOIN backend_inventorycontains IC on P.pid = IC.pid_id
                            WHERE ptype = "Food"
                            GROUP BY pid) AS PIN
                       LEFT OUTER JOIN 
                            (SELECT pid, SUM(oquantity) AS sout
                             FROM backend_product P LEFT OUTER JOIN backend_ordercontains OC on P.pid = OC.pid_id
                             WHERE ptype = "Food"
                             GROUP BY pid) AS POUT
                       ON PIN.pid = POUT.pid;
                       ''')
        res = dictfetchall(cursor)
        return convertNullToZero(res)

def convertNullToZero(dic):
    for row in dic:
        if (row['sin'] == None):
            row['sin'] = 0
        if (row['sout'] == None):
            row['sout'] = 0
        if (row['soh'] == None):
            row['soh'] = row['sin'] - row['sout']
    return dic