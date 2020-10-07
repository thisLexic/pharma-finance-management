# Generated by Django 3.0.6 on 2020-05-24 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0025_auto_20200524_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='retailer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='retailer_transactions', to=settings.AUTH_USER_MODEL),
        ),
    ]
