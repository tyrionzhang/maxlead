# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-18 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxlead_site', '0066_listingsbackcup'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryRankBackcup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_asin', models.CharField(max_length=50, verbose_name='User Asin')),
                ('asin', models.CharField(max_length=255, verbose_name='Asin')),
                ('cat', models.CharField(default='', max_length=255, verbose_name='Cat')),
                ('keywords', models.CharField(default='', max_length=255, verbose_name='Keywords')),
                ('rank', models.IntegerField(default=0, verbose_name='Rank')),
                ('is_ad', models.IntegerField(default=0, verbose_name='Ad')),
                ('created', models.DateTimeField(verbose_name='Created')),
            ],
            options={
                'db_table': 'category_rank_backcup',
            },
        ),
    ]
