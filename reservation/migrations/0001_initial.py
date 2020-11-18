# Generated by Django 3.1.1 on 2020-11-17 05:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('donation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dropoff_time_request', models.DateTimeField(default=django.utils.timezone.now)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donor_id', to=settings.AUTH_USER_MODEL)),
                ('helpseeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='helpseeker_id', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donation.resourcepost')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notificationstatus', models.IntegerField(choices=[(1, 'ACCEPT'), (2, 'REJECT'), (3, 'PENDING')], default=3)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_post', to='reservation.reservationpost')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noti_to_user', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noti_from_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]