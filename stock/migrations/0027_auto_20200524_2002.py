# Generated by Django 3.0.6 on 2020-05-24 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0026_auto_20200524_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='stock.Products'),
        ),
    ]
