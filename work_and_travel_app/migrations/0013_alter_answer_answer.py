# Generated by Django 4.2.9 on 2024-02-14 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work_and_travel_app', '0012_answer_answer_alter_answer_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work_and_travel_app.grade'),
        ),
    ]
