# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 06:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maxlead_site', '0050_auto_20180116_1434'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='groups',
            new_name='group',
        ),
    ]
