# Generated by Django 3.2.15 on 2023-01-20 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0057_alter_order_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
    ]
