# Generated by Django 5.0.3 on 2024-04-24 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargers', '0011_finishedchargingtransactionproxy_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargingtransaction',
            name='stop_reason',
            field=models.CharField(blank=True, choices=[('Local', 'Local'), ('Remote', 'Remote'), ('ConnectorError', 'Connector Error'), ('Other', 'Other')], max_length=40, null=True, verbose_name='Stop Reason'),
        ),
    ]