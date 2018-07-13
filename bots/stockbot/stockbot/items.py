# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from max_stock.models import WarehouseStocks,OrderItems


class WarehouseStocksItem(DjangoItem):
    # define the fields for your item here like:
    django_model = WarehouseStocks

class OrderItemsItem(DjangoItem):
    # define the fields for your item here like:
    django_model = OrderItems
