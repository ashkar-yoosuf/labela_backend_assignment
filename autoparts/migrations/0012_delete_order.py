# Generated by Django 4.1.1 on 2022-09-25 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autoparts', '0011_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]