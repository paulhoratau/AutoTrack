# Generated by Django 5.1.3 on 2024-12-12 13:44

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_keyhistory_operation_alter_keyhistory_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('serial', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('project_id', models.CharField(max_length=50)),
                ('license_plate', models.CharField(max_length=50)),
                ('zone', models.CharField(max_length=50)),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.car')),
            ],
            options={
                'ordering': ['serial'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('event_id', models.CharField(editable=False, max_length=100, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField()),
                ('type', models.CharField(choices=[('low', 'The accelerometer triggered a “low” event'), ('medium', 'The accelerometer triggered a “medium” event'), ('high', 'The accelerometer triggered a “high” event'), ('button', 'Button on the device was pressed'), ('input1', 'External cable input triggered an event'), ('start', 'Device started up'), ('stop', 'Device shutdown'), ('kl15_off', 'Ignition was turned off'), ('kl15_on', 'Ignition was turned on'), ('kl30_low', 'Power supply dropped below'), ('card_not_found', 'No SD card inserted'), ('flash_error', 'Internal flash overflow'), ('card_full', 'SD card full'), ('travel_start', 'The vehicle has been travelling for >10mph for at least 10 seconds'), ('travel_stop', 'The vehicle stopped travelling: speed dropped below 10mph for 10 seconds'), ('overspeed_start', "The vehicle's speed went above the overspeed threshold")], max_length=20)),
                ('booking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to='app.booking')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='app.car')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='app.device')),
                ('key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to='app.key')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('trip_id', models.CharField(editable=False, max_length=100, primary_key=True, serialize=False)),
                ('start', models.DateTimeField()),
                ('stop', models.DateTimeField()),
                ('mileage', models.IntegerField(help_text="Stored in METRES as that's what the API provides")),
                ('state', models.CharField(max_length=100)),
                ('booking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to='app.booking')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='app.car')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='app.device')),
                ('key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to='app.key')),
                ('parent_trip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_trips', to='app.trip')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-start'],
            },
        ),
    ]
