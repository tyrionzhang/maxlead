# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-31 07:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxlead_site', '0054_auto_20180123_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='asinreviews',
            name='is_done',
            field=models.IntegerField(default=0, null=True, verbose_name='Done'),
        ),
        migrations.AddField(
            model_name='questions',
            name='is_done',
            field=models.IntegerField(default=0, null=True, verbose_name='Done'),
        ),
    ]