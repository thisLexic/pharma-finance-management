# Generated by Django 3.0.6 on 2020-05-14 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_role_branches'),
        ('location', '0002_auto_20200514_1039'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Branche',
            new_name='Branches',
        ),
    ]
