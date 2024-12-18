# Generated by Django 5.1.3 on 2024-12-03 14:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_carreminder'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255, verbose_name='Town / City')),
                ('county', models.CharField(blank=True, max_length=50, null=True)),
                ('postcode', models.CharField(max_length=10)),
                ('latitude', models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='registration_number',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(db_index=True)),
                ('end_time', models.DateTimeField(blank=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='app.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to=settings.AUTH_USER_MODEL, verbose_name='driver')),
                ('end_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings_ending', to='app.location', verbose_name='Drop-off location')),
                ('start_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings_starting', to='app.location', verbose_name='Pick up location')),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(default='BMW', max_length=12)),
                ('model', models.CharField(default='E46', max_length=20)),
                ('year', models.PositiveIntegerField(default=2018)),
                ('engine', models.CharField(default='electric', max_length=8)),
                ('current_type', models.CharField(blank=True, max_length=2, null=True)),
                ('car_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carmodels', to='app.carclass')),
            ],
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('keycore_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_put_back', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('latest_operation', models.CharField(editable=False, max_length=7)),
                ('latest_status', models.CharField(editable=False, max_length=9)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keys', to='app.booking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keys', to=settings.AUTH_USER_MODEL, verbose_name='driver')),
            ],
        ),
        migrations.CreateModel(
            name='KeyHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(max_length=7)),
                ('status', models.CharField(max_length=9)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='app.key')),
            ],
        ),
    ]
