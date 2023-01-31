# Generated by Django 4.1 on 2023-01-31 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_bought'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productbid', to='auctions.listing'),
        ),
    ]
