# Generated by Django 4.1 on 2022-08-23 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_remove_auctionlisting_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='owner',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]