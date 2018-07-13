from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Thresholds(models.Model):
    sku = models.CharField('Sku',max_length=225)
    warehouse = models.CharField('Warehouse',max_length=225)
    threshold = models.IntegerField('Threshold',default=0)
    created = models.DateTimeField('Create Date', auto_now_add=True)

    class Meta:
        db_table = 'stock_thresholds'

class WarehouseStocks(models.Model):
    sku = models.CharField('Sku',max_length=225)
    warehouse = models.CharField('Warehouse', max_length=225)
    qty = models.IntegerField('Qty', default=0)
    is_new = models.IntegerField('Is New', default=1)
    created = models.DateTimeField('Create Date', auto_now_add=True)

    class Meta:
        db_table = 'warehouse_stocks'

class SkuUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sku = models.CharField('Sku',max_length=225)
    created = models.DateTimeField('Create Date', auto_now_add=True)

    class Meta:
        db_table = 'sku_users'

class StockLogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fun = models.CharField('Sku',max_length=225)
    description = models.TextField('Description')
    created = models.DateTimeField('Create Date', auto_now_add=True)

    class Meta:
        db_table = 'stock_logs'

class AmazonCode(models.Model):
    email = models.CharField('Email',max_length=225)
    code = models.CharField('Code',max_length=225)
    created = models.DateTimeField('Create Date', auto_now_add=True)

    class Meta:
        db_table = 'amazon_code'

class OrderItems(models.Model):
    order_id = models.CharField('Order Id', max_length=225)
    sku = models.CharField('SKU', max_length=50)
    order_status = models.CharField('Status', max_length=50)
    email = models.CharField('Email', max_length=50)
    is_email = models.IntegerField('Is Email', default=0)
    created = models.DateTimeField('Create Date', auto_now_add=True)

    class Meta:
        db_table = 'order_items'

class Templates(models.Model):
    sku = models.CharField('SKU', max_length=50)
    content = models.TextField('Content')
    created = models.DateTimeField('Create Date', auto_now_add=True)

    class Meta:
        db_table = 'templates'

class Schedule(models.Model):
    templates = models.ForeignKey(Templates, on_delete=models.CASCADE)
    sku = models.CharField('SKU', max_length=50)
    time_str = models.CharField('Time Str', max_length=50)
    created = models.DateTimeField('Create Date', auto_now_add=True)

    class Meta:
        db_table = 'schedule'

