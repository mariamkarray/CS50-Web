# Generated by Django 4.1 on 2022-08-20 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_auctionlisting_url_auctionlisting_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='bid',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]