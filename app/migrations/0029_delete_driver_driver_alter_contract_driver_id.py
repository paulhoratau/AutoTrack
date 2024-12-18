# Generated by Django 5.1.3 on 2024-12-17 16:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_driver_alter_contract_date_contract_driver_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Driver',
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('passport_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='Contract',
            name='driver_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver', to='app.driver'),
        ),
    ]