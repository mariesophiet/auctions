# Generated by Django 4.1 on 2023-01-26 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_date_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='img',
            field=models.ImageField(default='/media/images/placeholder.svg', upload_to='images'),
        ),
    ]
