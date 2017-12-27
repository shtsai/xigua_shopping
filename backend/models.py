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

    def __str__(self):
        return self.oid
