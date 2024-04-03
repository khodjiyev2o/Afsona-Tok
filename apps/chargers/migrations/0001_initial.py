# Generated by Django 5.0.3 on 2024-04-03 17:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0003_connectiontype_country_support_alter_usercar_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargePoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('charger_id', models.CharField(max_length=50, verbose_name='Charger ID')),
                ('last_boot_notification', models.DateTimeField(blank=True, null=True, verbose_name='Last Boot Notification')),
                ('last_heartbeat', models.DateTimeField(blank=True, null=True, verbose_name='Last Heartbeat')),
                ('is_connected', models.BooleanField(default=False, verbose_name='is Connected')),
                ('is_visible_in_mobile', models.BooleanField(default=True)),
                ('max_electric_power', models.IntegerField(default=0, verbose_name="ChargePoint's Max electric power")),
            ],
            options={
                'verbose_name': 'ChargePoint',
                'verbose_name_plural': 'ChargePoints',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Connector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=40, null=True, verbose_name='Name')),
                ('connector_id', models.IntegerField(verbose_name='Connector Id within Charger')),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Preparing', 'Preparing'), ('Charging', 'Charging'), ('SuspendedEVSE', 'Suspended Evse'), ('SuspendedEV', 'Suspended Ev'), ('Finishing', 'Finishing'), ('Reserved', 'Reserved'), ('Unavailable', 'Unavailable'), ('Faulted', 'Faulted')], default='Unavailable', max_length=50, verbose_name='Статус')),
                ('charge_point', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chargers.chargepoint')),
                ('standard', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.connectiontype', verbose_name="Connector's standard")),
            ],
            options={
                'verbose_name': 'Connector',
                'verbose_name_plural': 'Connectors',
                'ordering': ['-id'],
                'unique_together': {('charge_point', 'connector_id')},
            },
        ),
        migrations.CreateModel(
            name='ChargingTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('battery_percent_on_start', models.IntegerField(default=0, verbose_name='Battery Percent on Start')),
                ('battery_percent_on_end', models.IntegerField(blank=True, null=True, verbose_name='Battery Percent on End')),
                ('meter_on_start', models.IntegerField(verbose_name='Meter On Start')),
                ('meter_on_end', models.IntegerField(blank=True, null=True, verbose_name='Meter on End')),
                ('meter_used', models.IntegerField(default=0, verbose_name='Meter Used')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total Price')),
                ('status', models.CharField(choices=[('IN_PROGRESS', 'In Progress'), ('FINISHED', 'Finished')], default='IN_PROGRESS', max_length=30, verbose_name='Status')),
                ('start_reason', models.CharField(blank=True, choices=[('LOCAL', 'Local'), ('REMOTE', 'Remote')], max_length=40, null=True, verbose_name='Start Reason')),
                ('stop_reason', models.CharField(blank=True, choices=[('LOCAL', 'Local'), ('REMOTE', 'Remote'), ('OTHER', 'Other')], max_length=40, null=True, verbose_name='Stop Reason')),
                ('is_limited', models.BooleanField(default=False, verbose_name='Is Limited')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('user_car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.usercar', verbose_name='User Car')),
                ('connector', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chargers.connector', verbose_name='Connector')),
            ],
            options={
                'verbose_name': 'ChargingTransaction',
                'verbose_name_plural': 'ChargingTransactions',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('address', models.CharField(max_length=100, verbose_name='Address')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Longitude')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Latitude')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.district', verbose_name='District')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='chargepoint',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chargers.location', verbose_name='Location'),
        ),
        migrations.CreateModel(
            name='UserFavouriteLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chargers.location', verbose_name='Location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
