# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 07:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxlead_site', '0007_auto_20171129_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asinreviews',
            name='negative_keywords',
            field=models.TextField(null=True, verbose_name='Negative Keywords'),
        ),
        migrations.AlterField(
            model_name='asinreviews',
            name='positive_keywords',
            field=models.TextField(null=True, verbose_name='Positive Keywords'),
        ),
    ]
