# Generated by Django 4.2.5 on 2024-01-03 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='session_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]