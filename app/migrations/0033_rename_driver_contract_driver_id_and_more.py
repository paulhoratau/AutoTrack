# Generated by Django 5.1.3 on 2024-12-18 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_rename_driver_id_contract_driver'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='driver',
            new_name='driver_id',
        ),
        migrations.RenameField(
            model_name='contract',
            old_name='contractor',
            new_name='user_id',
        ),
    ]
