# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 02:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxlead_site', '0016_auto_20171212_1035'),
    ]

    operations = [

        migrations.AlterModelTable(
            name='log',
            table='log',
        ),
        migrations.AlterModelTable(
            name='userprofile',
            table='user_profile',
        ),
    ]
