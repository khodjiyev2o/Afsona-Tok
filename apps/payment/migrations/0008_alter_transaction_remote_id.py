# Generated by Django 5.0.3 on 2024-04-17 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_alter_merchantrequestlog_request_body_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='remote_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Remote id'),
        ),
    ]