# Generated by Django 4.2.9 on 2024-01-27 21:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('work_and_travel_app', '0004_rename_userprofile_baseinformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseinformation',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]