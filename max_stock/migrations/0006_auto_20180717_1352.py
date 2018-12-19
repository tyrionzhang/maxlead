# Generated by Django 2.0.6 on 2018-07-17 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('max_stock', '0005_auto_20180717_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menus',
            name='users',
        ),
        migrations.RemoveField(
            model_name='roles',
            name='menus',
        ),
        migrations.AddField(
            model_name='menus',
            name='roles',
            field=models.ManyToManyField(to='max_stock.Roles'),
        ),
        migrations.AlterField(
            model_name='roles',
            name='code',
            field=models.CharField(max_length=50, verbose_name='Code'),
        ),
    ]
