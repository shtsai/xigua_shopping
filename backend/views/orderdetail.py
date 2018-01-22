from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.db import connection
from django.contrib.auth.decorators import login_required
from backend.models import Customer, Order, Product, Inventory
from .util import *


def orderdetail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    template_name = 'backend/order_detail.html'
    items = get_order_items(order_id)
    customer = Customer.objects.filter(order__oid=order_id)[0]
    return render(request, template_name, {
        'order': order,
        'items': items,
        'customer': customer,
    })

def get_order_items(order_id):
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT *
                        FROM backend_order AS O JOIN backend_ordercontains AS OC ON O.oid = OC.oid_id JOIN backend_product AS P ON P.pid = OC.pid_id
                        WHERE O.oid = %s
                        ''', [order_id])
        res = dictfetchall(cursor)
        return res

def addpayment(request):
    order = Order.objects.filter(oid=request.POST['oid'])[0]
    order.opaid = 1
    order.ototal = request.POST['total']
    order.opaymentmethod = request.POST['paymentmethod']
    order.ostatus = "paid"
    order.save()
    return redirect("/order/" + str(request.POST['oid']))
