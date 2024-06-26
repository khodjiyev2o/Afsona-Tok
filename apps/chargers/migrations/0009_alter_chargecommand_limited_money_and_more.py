# Generated by Django 5.0.3 on 2024-04-16 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargers', '0008_chargecommand_is_limited_chargecommand_limit_sum_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargecommand',
            name='limited_money',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Limited money'),
        ),
        migrations.AlterField(
            model_name='chargingtransaction',
            name='limited_money',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Limited money'),
        ),
    ]
