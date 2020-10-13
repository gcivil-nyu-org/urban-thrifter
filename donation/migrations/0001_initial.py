# Generated by Django 3.1.1 on 2020-10-12 18:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResourcePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('dropoff_time_1', models.DateTimeField(default=django.utils.timezone.now)),
                ('dropoff_time_2', models.DateTimeField(default=django.utils.timezone.now)),
                ('dropoff_time_3', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('dropoff_location', models.TextField()),
                ('resource_category', models.CharField(choices=[('Food', 'Food'), ('Medical', 'Medical/ PPE'), ('Clothing', 'Clothing/ Covers'), ('Electronics', 'Electronics'), ('Others', 'Others')], default='Food', max_length=100)),
                ('status', models.CharField(choices=[('AVAILABLE', 'Available'), ('PENDING', 'Pending'), ('NOTAVAILABLE', 'Not Available')], default='Available', max_length=100)),
            ],
        ),
    ]