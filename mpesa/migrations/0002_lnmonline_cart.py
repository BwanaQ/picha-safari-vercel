# Generated by Django 4.2.5 on 2024-01-24 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_cart_session_id'),
        ('mpesa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lnmonline',
            name='cart',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='cart.cart'),
        ),
    ]