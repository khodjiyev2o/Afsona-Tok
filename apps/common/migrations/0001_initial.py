# Generated by Django 3.0.8 on 2023-09-18 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FrontendTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('key', models.CharField(max_length=255, unique=True, verbose_name='Key')),
                ('text', models.CharField(max_length=1024, verbose_name='Text')),
            ],
            options={
                'verbose_name': 'Frontend translation',
                'verbose_name_plural': 'Frontend translations',
            },
        )
    ]
