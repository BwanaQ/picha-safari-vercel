# Generated by Django 4.2.5 on 2024-01-24 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0002_lnmonline_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='lnmonline',
            name='Amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lnmonline',
            name='Balance',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='lnmonline',
            name='CheckoutRequestID',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='lnmonline',
            name='MerchantRequestID',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='lnmonline',
            name='MpesaReceiptNumber',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='lnmonline',
            name='PhoneNumber',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AddField(
            model_name='lnmonline',
            name='ResultCode',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lnmonline',
            name='ResultDesc',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='lnmonline',
            name='TransactionDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]