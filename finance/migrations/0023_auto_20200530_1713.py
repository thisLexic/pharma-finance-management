# Generated by Django 3.0.6 on 2020-05-30 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0022_sales_bank'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='OR_nums',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='caja_minus_deposit',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='num_cstmr',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='num_rcpt',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='num_trxn',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='petty_cash',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='total_disc',
            field=models.FloatField(null=True),
        ),
    ]