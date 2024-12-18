# Generated by Django 5.1.3 on 2024-12-12 14:26

import django.utils.timezone
import model_utils.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_car_location_alter_car_model_alter_car_vin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='vin',
        ),
        migrations.AddField(
            model_name='car',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='car',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
    ]
