# Generated by Django 4.2.9 on 2024-02-05 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_and_travel_app', '0006_remove_grade_rating_grade_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseinformation',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]
