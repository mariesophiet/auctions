# Generated by Django 4.1 on 2022-08-23 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_comments_bids'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='img',
            field=models.ImageField(default=None, upload_to='media'),
        ),
    ]