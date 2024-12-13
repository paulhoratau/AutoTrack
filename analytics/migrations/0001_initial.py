# Generated by Django 5.1.3 on 2024-12-10 16:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0022_alter_keyhistory_operation_alter_keyhistory_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('serial', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('project_id', models.CharField(max_length=50)),
                ('license_plate', models.CharField(max_length=50)),
                ('zone', models.CharField(max_length=50)),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.car')),
            ],
            options={
                'ordering': ['serial'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.CharField(editable=False, max_length=100, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField()),
                ('type', models.CharField(choices=[('low', 'The accelerometer triggered a “low” event'), ('medium', 'The accelerometer triggered a “medium” event'), ('high', 'The accelerometer triggered a “high” event'), ('button', 'Button on the device was pressed'), ('input1', 'External cable input triggered an event'), ('start', 'Device started up'), ('stop', 'Device shutdown'), ('kl15_off', 'Ignition was turned off'), ('kl15_on', 'Ignition was turned on'), ('kl30_low', 'Power supply dropped below'), ('card_not_found', 'No SD card inserted'), ('flash_error', 'Internal flash overflow'), ('card_full', 'SD card full'), ('travel_start', 'The vehicle has been travelling for >10mph for at least 10 seconds'), ('travel_stop', 'The vehicle stopped travelling: speed dropped below 10mph for 10 seconds'), ('overspeed_start', "The vehicle's speed went above the overspeed threshold")], max_length=20)),
                ('booking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to='app.booking')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='app.car')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='analytics.device')),
                ('key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to='app.key')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('trip_id', models.CharField(editable=False, max_length=100, primary_key=True, serialize=False)),
                ('start', models.DateTimeField()),
                ('stop', models.DateTimeField()),
                ('mileage', models.IntegerField(help_text="Stored in METRES as that's what the API provides")),
                ('state', models.CharField(max_length=100)),
                ('booking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to='app.booking')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='app.car')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='analytics.device')),
                ('key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to='app.key')),
                ('parent_trip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_trips', to='analytics.trip')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-start'],
            },
        ),
    ]
