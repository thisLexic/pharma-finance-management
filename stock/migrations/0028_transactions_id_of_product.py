# Generated by Django 3.0.6 on 2020-05-24 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0027_auto_20200524_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='id_of_product',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
