# Generated by Django 4.2.6 on 2023-10-14 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_rename_role_workingday_shift'),
    ]

    operations = [
        migrations.AddField(
            model_name='workingday',
            name='reserved',
            field=models.BooleanField(default=False),
        ),
    ]
