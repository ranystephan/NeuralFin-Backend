# Generated by Django 4.1.7 on 2023-05-05 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_stock_currency_stock_exchange_stock_industry_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='exchange',
            new_name='index',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='currency',
        ),
        migrations.AddField(
            model_name='stock',
            name='country',
            field=models.CharField(default='USA', max_length=10),
        ),
    ]