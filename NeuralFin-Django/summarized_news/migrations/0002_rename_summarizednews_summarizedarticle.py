# Generated by Django 4.1.7 on 2023-03-05 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summarized_news', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SummarizedNews',
            new_name='SummarizedArticle',
        ),
    ]
