# Generated by Django 3.0.6 on 2020-05-20 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20200520_0356'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchases',
            old_name='invoice_image',
            new_name='invoice_file',
        ),
    ]
