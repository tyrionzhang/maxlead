# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 06:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxlead_site', '0006_auto_20171129_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asinreviews',
            name='created',
            field=models.DateField(auto_now_add=True, verbose_name='Create Date'),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='created',
            field=models.DateField(auto_now_add=True, verbose_name='Create Date'),
        ),
    ]
