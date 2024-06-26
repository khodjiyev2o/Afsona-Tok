# Generated by Django 5.0.3 on 2024-04-03 17:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('is_for_everyone', models.BooleanField(default=False, verbose_name='Is for everyone')),
                ('users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Users')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'db_table': 'Notification',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_sent', models.BooleanField(default=False, verbose_name='Is sent')),
                ('is_read', models.BooleanField(default=False, verbose_name='Is read')),
                ('sent_at', models.DateTimeField(blank=True, null=True, verbose_name='Sent At')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_notifications', to='notification.notification', verbose_name='User notification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_notifications', to=settings.AUTH_USER_MODEL, verbose_name='User id')),
            ],
            options={
                'verbose_name': 'UserNotification',
                'verbose_name_plural': 'UserNotifications',
                'db_table': 'UserNotification',
                'ordering': ('created_at',),
            },
        ),
    ]
