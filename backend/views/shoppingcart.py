from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.db import connection
from django.contrib.auth.decorators import login_required
from backend.models import Customer, Order, Product, Inventory, Ordercontains
from .util import *

def newshoppingcart(request):
    order = createNewOrder()
    return redirect("/shoppingcart/" + str(order.oid))

def shoppingcart(request, order_id):
    template_name = 'backend/shoppingcart.html'
    
    return render(request, template_name, {
        'order': get_object_or_404(Order, pk=order_id),
        'items': get_order_items(order_id),
        'foodproduct': get_food_products(),
        'healthproduct': Product.objects.filter(ptype="Health"),
    })

def createNewOrder():
    order = Order.create()
    return order

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

def get_order_items(order_id):
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT *
                        FROM backend_order AS O JOIN backend_ordercontains AS OC ON O.oid = OC.oid_id JOIN backend_product AS P ON P.pid = OC.pid_id
                        WHERE O.oid = %s
                        ORDER BY P.pid
                        ''', [order_id])
        res = dictfetchall(cursor)
        return res


def convertNullToZero(dic):
    for row in dic:
        if (row['sin'] == None):
            row['sin'] = 0
        if (row['sout'] == None):
            row['sout'] = 0
        if (row['soh'] == None):
            row['soh'] = row['sin'] - row['sout']
    return dic


def addtocart(request):
    order = Order.objects.filter(oid=request.POST['oid'])[0]
    product = Product.objects.filter(pid=request.POST['pid'])[0]
    quantity = request.POST['quantity']
    price = request.POST['price']

    exist = Ordercontains.objects.filter(oid=order, pid=product)
    # The same product has been included in this order
    # Delete previous record to overwrite
    if exist:
        exist.delete()
    Ordercontains.create(order, product, quantity, price)

    return redirect("/shoppingcart/" + str(request.POST['oid']))

def removefromcart(request):
    order = Order.objects.filter(oid=request.POST['oid'])[0]
    product = Product.objects.filter(pid=request.POST['pid'])[0]

    exist = Ordercontains.objects.filter(oid=order, pid=product)
    if exist:
        exist.delete()

    return redirect("/shoppingcart/" + str(request.POST['oid']))

def selectcustomer(request):
    customer = Customer.objects.all();
    template_name = 'backend/selectcustomer.html'
    return render(request, template_name, {
        'customers': customer,    
        'oid': request.POST['oid'],
    })

def setcustomer(request):
    if ('new' in request.POST):
        customer = Customer.create(request.POST['name'])
        if (request.POST['wechat'] != ""):
            customer.cwechat = request.POST['wechat']
        if (request.POST['phone'] != ""):
            customer.cphone = request.POST['phone']
        if (request.POST['address'] != ""):
            customer.caddr = request.POST['address']
        if (request.POST['note'] != ""):
            customer.cnote = request.POST['note']
        customer.save()
    else:
        customer = Customer.objects.filter(cid=request.POST['cid'])[0]
    
    order = Order.objects.filter(oid=request.POST['oid'])[0]
    order.cid_id = customer
    order.save()
    return redirect("/order/" + str(request.POST['oid']))
