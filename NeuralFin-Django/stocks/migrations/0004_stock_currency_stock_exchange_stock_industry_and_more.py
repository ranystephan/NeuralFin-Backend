# Generated by Django 4.1.7 on 2023-05-04 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='currency',
            field=models.CharField(default='USD', max_length=10),
        ),
        migrations.AddField(
            model_name='stock',
            name='exchange',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AddField(
            model_name='stock',
            name='industry',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='sector',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='stock',
            name='symbol',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
