# Generated by Django 3.0.6 on 2020-06-18 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0040_auto_20200618_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='bimonthly_in',
            name='giv_a',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bimonthly_in',
            name='giv_a_desc',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='bimonthly_in',
            name='giv_b',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bimonthly_in',
            name='giv_b_desc',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='bimonthly_in',
            name='giv_c',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bimonthly_in',
            name='giv_c_desc',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='bimonthly_in',
            name='giv_d',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bimonthly_in',
            name='giv_d_desc',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]