# Generated by Django 4.1.1 on 2022-09-25 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autoparts', '0009_order_delete_delivery'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]