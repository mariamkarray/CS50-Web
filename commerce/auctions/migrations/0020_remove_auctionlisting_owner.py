# Generated by Django 4.1 on 2022-08-23 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_alter_auctionlisting_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='owner',
        ),
    ]
