# Generated by Django 3.0.6 on 2020-05-23 02:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0013_auto_20200523_1052'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PurchasePaymentMethod',
            new_name='Purchase_Payment_Method',
        ),
    ]
