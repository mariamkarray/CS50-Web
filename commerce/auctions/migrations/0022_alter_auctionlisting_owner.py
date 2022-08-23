# Generated by Django 4.1 on 2022-08-23 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_auctionlisting_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
