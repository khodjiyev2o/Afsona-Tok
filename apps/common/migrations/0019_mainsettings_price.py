# Generated by Django 5.0.3 on 2024-06-03 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0018_remove_mainsettings_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainsettings',
            name='price',
            field=models.DecimalField(decimal_places=2, default=2500, max_digits=10, verbose_name='Price for 1 kwt of electricity'),
        ),
    ]
