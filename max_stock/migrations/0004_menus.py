# Generated by Django 2.0.6 on 2018-07-16 17:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('max_stock', '0003_auto_20180712_1005'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('url', models.CharField(max_length=50, verbose_name='Url')),
                ('elem_id', models.CharField(max_length=50, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Menus',
            },
        ),
    ]
