# Generated by Django 3.0.6 on 2020-05-24 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0024_auto_20200524_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='date',
            field=models.DateField(blank=True, editable=False),
        ),
    ]