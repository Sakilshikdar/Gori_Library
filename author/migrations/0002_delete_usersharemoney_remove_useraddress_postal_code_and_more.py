# Generated by Django 4.2.7 on 2023-12-29 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserShareMoney',
        ),
        migrations.RemoveField(
            model_name='useraddress',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='userbankaccount',
            name='account_type',
        ),
        migrations.RemoveField(
            model_name='userbankaccount',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='userbankaccount',
            name='gender_type',
        ),
    ]
