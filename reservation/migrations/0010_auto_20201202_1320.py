# Generated by Django 3.1.1 on 2020-12-02 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0009_auto_20201202_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationpost',
            name='dropoff_time_request',
            field=models.DateTimeField(),
        ),
    ]
