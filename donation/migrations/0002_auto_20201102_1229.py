# Generated by Django 3.1.1 on 2020-11-02 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("donation", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resourcepost",
            name="donor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
