# Generated by Django 4.1 on 2022-08-23 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auctionlisting_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='owner',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
