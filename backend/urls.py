from django.urls import path

from . import views

app_name = 'backend'
urlpatterns = [
    path('', views.index, name='index'),
    path('customer/', views.CustomerView.as_view(), name='customer'),
    path('customer/<int:customer_id>/', views.customerdetail, name='customer_detail'),
    path('product/', views.product, name='product'),
    path('product/<int:product_id>/', views.productdetail, name='product_detail'),
    path('order/', views.order, name='order'),
    path('order/<int:order_id>/', views.orderdetail, name='order_detail'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/<int:inventory_id>', views.inventorydetail, name='inventory_detail'),
    path('addtocart/<int:product_id>/', views.addtocart, name='addtocart'),
]
