# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-05 02:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxlead_site', '0043_listingwacher_seller_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingwacher',
            name='seller_link',
            field=models.CharField(default='', max_length=225, null=True, verbose_name='Seller Link'),
        ),
    ]