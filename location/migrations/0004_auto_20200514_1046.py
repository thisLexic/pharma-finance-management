# Generated by Django 3.0.6 on 2020-05-14 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_auto_20200514_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branches',
            name='location',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
