# Generated by Django 4.2.6 on 2023-10-30 11:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0010_alter_workingday_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workingday',
            unique_together={('date', 'time_slot', 'barber')},
        ),
    ]
