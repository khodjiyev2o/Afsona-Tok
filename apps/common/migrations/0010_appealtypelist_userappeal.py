# Generated by Django 5.0.3 on 2024-04-20 11:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0009_alter_mainsettings_user_minimum_balance"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AppealTypeList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "name_uz",
                    models.CharField(max_length=255, null=True, verbose_name="Name"),
                ),
                (
                    "name_ru",
                    models.CharField(max_length=255, null=True, verbose_name="Name"),
                ),
                (
                    "name_en",
                    models.CharField(max_length=255, null=True, verbose_name="Name"),
                ),
            ],
            options={
                "verbose_name": "Appeal Type",
                "verbose_name_plural": "Appeal Types",
            },
        ),
        migrations.CreateModel(
            name="UserAppeal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="appeals",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "User Appeal",
                "verbose_name_plural": "User Appeals",
            },
        ),
    ]
