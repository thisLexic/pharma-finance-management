# Generated by Django 3.0.6 on 2020-05-14 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_auto_20200514_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='roles',
            name='is_assistant',
            field=models.BooleanField(default=False),
        ),
    ]
