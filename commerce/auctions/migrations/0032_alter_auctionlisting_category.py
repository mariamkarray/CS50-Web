# Generated by Django 4.1 on 2022-08-23 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0031_alter_auctionlisting_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.categories'),
        ),
    ]
