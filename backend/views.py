from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db import connection
from .models import Customer, Order, Product, Inventory

def index(request):
    return render(request, 'backend/index.html')

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
    foodproduct = Product.objects.filter(ptype="Food")
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

def productdetail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    template_name = 'backend/product_detail.html'
    return render(request, template_name, {
        'product': product,
    })
    
def order(request):
    order = get_all_orders()
    pendingorder = get_pending_orders()
    shippedorder = get_shipped_orders()
    completedorder = get_completed_orders()
    template_name = 'backend/order.html'
    return render(request, template_name, {
        'order': order,    
        'pendingorder': pendingorder,
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
                        WHERE ostatus="Pending"
                        ORDER BY O.odate DESC 
                        ''')
        res = dictfetchall(cursor)
        return res

def get_shipped_orders():
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT *
                        FROM backend_order AS O JOIN backend_customer AS C ON O.cid_id = C.cid
                        WHERE ostatus="Shipped"
                        ORDER BY O.odate DESC 
                        ''')
        res = dictfetchall(cursor)
        return res
    
def get_completed_orders():
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT *
                        FROM backend_order AS O JOIN backend_customer AS C ON O.cid_id = C.cid
                        WHERE ostatus="Completed"
                        ORDER BY O.odate DESC 
                        ''')
        res = dictfetchall(cursor)
        return res

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


def inventory(request):
    inventory = Inventory.objects.all()
    template_name = 'backend/inventory.html'
    return render(request, template_name, {
        'inventory': inventory,
    })

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

def addtocart(request, product_id):
    if not (str(product_id) in request.session):
        request.session['cart'][str(product_id)] = 1
    else:
        request.session['cart'][str(product_id)] += 1
    return product(request)

