# Generated by Django 3.0.6 on 2020-05-23 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0010_roles_sale_staff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roles',
            old_name='sale_staff',
            new_name='sale_branches',
        ),
    ]
