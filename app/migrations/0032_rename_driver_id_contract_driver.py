# Generated by Django 5.1.3 on 2024-12-18 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_rename_contractor_id_contract_contractor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='driver_id',
            new_name='driver',
        ),
    ]