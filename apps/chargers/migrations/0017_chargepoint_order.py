# Generated by Django 5.0.3 on 2024-05-12 11:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chargers", "0016_ocppservicerequestresponselogs"),
    ]

    operations = [
        migrations.AddField(
            model_name="chargepoint",
            name="order",
            field=models.IntegerField(default=0, verbose_name="Order"),
        ),
    ]
