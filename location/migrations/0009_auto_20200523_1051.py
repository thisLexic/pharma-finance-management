# Generated by Django 3.0.6 on 2020-05-23 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0008_auto_20200523_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branches',
            name='location',
            field=models.CharField(max_length=256),
        ),
        migrations.AddConstraint(
            model_name='branches',
            constraint=models.UniqueConstraint(fields=('manager', 'location'), name='unique branch'),
        ),
    ]
