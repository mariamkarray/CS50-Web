# Generated by Django 4.1 on 2022-08-21 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auctionlisting_bids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='bids',
        ),
    ]
