# Generated by Django 4.2.6 on 2023-10-18 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_workingday_is_vacation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingday',
            name='time_slot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schedule.timeslot'),
        ),
    ]
