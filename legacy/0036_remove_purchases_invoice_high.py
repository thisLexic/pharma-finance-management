# Generated by Django 3.0.6 on 2020-06-01 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0035_auto_20200601_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchases',
            name='invoice_high',
        ),
    ]