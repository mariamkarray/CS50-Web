# Generated by Django 4.1 on 2022-08-24 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0032_alter_auctionlisting_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(max_length=64),
        ),
    ]
