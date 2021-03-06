# Generated by Django 2.0.6 on 2018-07-17 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('max_stock', '0004_menus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('code', models.CharField(max_length=50, verbose_name='Url')),
            ],
            options={
                'db_table': 'roles',
            },
        ),
        migrations.AlterModelTable(
            name='menus',
            table='menus',
        ),
        migrations.AddField(
            model_name='roles',
            name='menus',
            field=models.ManyToManyField(to='max_stock.Menus'),
        ),
    ]
