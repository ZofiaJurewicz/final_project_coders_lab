# Generated by Django 4.2.9 on 2024-02-06 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work_and_travel_app', '0008_offer_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='time',
        ),
    ]
