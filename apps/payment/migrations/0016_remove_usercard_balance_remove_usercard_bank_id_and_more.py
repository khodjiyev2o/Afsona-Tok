# Generated by Django 5.0.3 on 2024-04-23 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0015_alter_usercard_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercard',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='usercard',
            name='bank_id',
        ),
        migrations.RemoveField(
            model_name='usercard',
            name='processing',
        ),
        migrations.RemoveField(
            model_name='usercard',
            name='vendor',
        ),
    ]
