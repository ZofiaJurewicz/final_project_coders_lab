# Generated by Django 4.2.9 on 2024-02-15 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_and_travel_app', '0014_rename_grade_answer_grade_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseinformation',
            name='date_of_birth',
            field=models.DateField(help_text='Enter date: YYYY-MM-DD'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='since_when',
            field=models.DateField(help_text='Enter date: YYYY-MM-DD'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='until_when',
            field=models.DateField(help_text='Enter date: YYYY-MM-DD'),
        ),
    ]
