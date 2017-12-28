from django.db import models
from django.utils import timezone

import datetime

class Customer(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField('Name', max_length=20)
    caddr = models.CharField('Address', max_length=50, null=True)
    cphone = models.CharField('Phone', max_length=15, null=True)
    cwechat = models.CharField('Wechat', max_length=20, null=True)
    cdate = models.DateTimeField('Date Created')
    cnote = models.CharField('Note', max_length=100, null=True)

    def __str__(self):
        return self.cname

class Order(models.Model):
    oid = models.CharField(max_length=30, primary_key=True)
    cid = models.ForeignKey('Customer', on_delete=models.CASCADE)
    odate = models.DateTimeField('Date Ordered')
    oshipdate = models.DateTimeField('Date Shipped', null=True)
    opaid = models.BooleanField('Is this order paid?')
    ototal = models.DecimalField('Total amount', max_digits=10, decimal_places=2, null=True)
    opaymentmethod = models.CharField('Payment method', max_length=20, null=True)
    ostatus = models.CharField('Status', max_length=20)
    onote = models.CharField('Note', max_length=100, null=True)

    def __str__(self):
        return self.oid

class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    pname = models.CharField('Product Name', max_length=40)
    ptype = models.CharField('Product Type', max_length=20, null=True)
    pcost = models.DecimalField('Product Cost', max_digits=10, decimal_places=2, null=True)
    pprice = models.DecimalField('Product Price', max_digits=10, decimal_places=2, null=True)
    pnote = models.CharField('Note', max_length=100, null=True)

    def __str__(self):
        return self.pname

class Ordercontains(models.Model):
    oid = models.ForeignKey('Order', on_delete=models.CASCADE)
    pid = models.ForeignKey('Product', on_delete=models.CASCADE)
    oquantity = models.IntegerField('Order Quantity')
    oprice = models.DecimalField('Order Price', max_digits=10, decimal_places=2)

    class Meta:
        unique_together = (('oid', 'pid'))
    def __str__(self):
        return str(self.oid) + " " + str(self.pid)


class Inventory(models.Model):
    iid = models.AutoField(primary_key=True)
    idate = models.DateTimeField('Date Received')
    icost = models.DecimalField('Total Value', max_digits=10, decimal_places=2)
    ishipping = models.DecimalField('Shipping Cost', max_digits=10, decimal_places=2)
    itype = models.CharField('Shipping Method', max_length=20, null=True)
    inote = models.CharField('Note', max_length=100, null=True)

    def __str__(self):
        return str(self.iid)
