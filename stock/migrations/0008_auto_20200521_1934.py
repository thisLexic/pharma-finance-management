# Generated by Django 3.0.6 on 2020-05-21 11:34

from django.db import migrations
import private_storage.fields
import private_storage.storage.files
import stock.models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0007_auto_20200521_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchases',
            name='invoice_file',
            field=private_storage.fields.PrivateFileField(blank=True, null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=stock.models.Purchases.invoice_user_directory_path),
        ),
        migrations.AlterField(
            model_name='purchases',
            name='proof_of_payment',
            field=private_storage.fields.PrivateFileField(blank=True, null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=stock.models.Purchases.payment_user_directory_path),
        ),
    ]
