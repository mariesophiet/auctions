# Generated by Django 4.1 on 2023-01-26 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listing_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='img',
            field=models.ImageField(blank=True, default='C:/Users/marie/OneDrive/CS50/commerce/media/images/oscar.jpg', null=True, upload_to='images'),
        ),
    ]