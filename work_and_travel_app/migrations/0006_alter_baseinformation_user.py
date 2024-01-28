# Generated by Django 4.2.9 on 2024-01-27 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('work_and_travel_app', '0005_baseinformation_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseinformation',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
