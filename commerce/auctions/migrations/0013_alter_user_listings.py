# Generated by Django 4.1 on 2022-08-22 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_user_listings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='listings',
            field=models.ManyToManyField(blank=True, related_name='users', to='auctions.auctionlisting'),
        ),
    ]
