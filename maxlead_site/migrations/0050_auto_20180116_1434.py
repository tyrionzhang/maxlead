# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 06:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maxlead_site', '0049_auto_20180108_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='maxlead_site.UserProfile'),
        ),
        migrations.AlterField(
            model_name='listings',
            name='user_asin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='maxlead_site.UserAsins'),
        ),
        migrations.RemoveField(
            model_name='menbergroups',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='group',
        ),
        migrations.DeleteModel(
            name='MenberGroups',
        ),
    ]