# Generated by Django 4.2.6 on 2023-10-17 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_remove_schedule_barber_workingday_barber_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='workingday',
            name='is_vacation',
            field=models.BooleanField(default=False),
        ),
    ]
