# Generated by Django 4.1 on 2022-08-23 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_auctionlisting_closed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='listing',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auctions.auctionlisting'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bids',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bids',
            name='value',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
