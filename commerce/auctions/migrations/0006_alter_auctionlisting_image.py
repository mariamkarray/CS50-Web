# Generated by Django 4.1 on 2022-08-20 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_auctionlisting_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
