from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db import connection
from .models import Customer, Order, Product

# Create your views here.

def index(request):
    return HttpResponse("Hello world")

class CustomerView(generic.ListView):
    template_name = 'backend/customer.html'
    context_object_name = 'customer_list'

    def get_queryset(self):
        return Customer.objects.raw('SELECT * FROM backend_customer ORDER BY cid')


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

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def product(request):
    product = Product.objects.all()
    template_name = 'backend/product.html'
    return render(request, template_name, {
        'product': product,
    })

def productdetail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    template_name = 'backend/product_detail.html'
    return render(request, template_name, {
        'product': product,
    })
    
def order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    template_name = 'backend/order.html'
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
