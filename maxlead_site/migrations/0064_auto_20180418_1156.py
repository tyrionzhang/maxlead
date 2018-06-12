# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-18 03:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maxlead_site', '0063_auto_20180418_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswersBackcup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qid', models.IntegerField(default=0, verbose_name='Qid')),
                ('person', models.CharField(max_length=225, verbose_name='Person')),
                ('answer', models.TextField(null=True, verbose_name='Answer')),
                ('created', models.DateTimeField(verbose_name='Create Date')),
            ],
            options={
                'db_table': 'answers_backcup',
            },
        ),
        migrations.CreateModel(
            name='QuestionsBackcup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qid', models.IntegerField(default=0, verbose_name='qid')),
                ('question', models.TextField(null=True, verbose_name='Question')),
                ('asin', models.CharField(default='', max_length=50, verbose_name='AsinId')),
                ('asked', models.CharField(default='', max_length=225, verbose_name='Asked')),
                ('votes', models.IntegerField(default=0, null=True, verbose_name='Votes')),
                ('count', models.IntegerField(default=0, null=True, verbose_name='Count')),
                ('is_done', models.IntegerField(default=0, null=True, verbose_name='Done')),
                ('created', models.DateTimeField(verbose_name='Create Date')),
            ],
            options={
                'db_table': 'questions_backcup',
            },
        ),
        migrations.AddField(
            model_name='asinreviewsbackcup',
            name='ar_id',
            field=models.IntegerField(default=0, verbose_name='ar_id'),
        ),
        migrations.AddField(
            model_name='reviewsbackcup',
            name='rid',
            field=models.IntegerField(default=0, verbose_name='Rid'),
        ),
    ]