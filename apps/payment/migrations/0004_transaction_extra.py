# Generated by Django 5.0.3 on 2024-04-16 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_transaction_canceled_at_alter_transaction_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='extra',
            field=models.JSONField(blank=True, null=True, verbose_name='Extra'),
        ),
    ]
