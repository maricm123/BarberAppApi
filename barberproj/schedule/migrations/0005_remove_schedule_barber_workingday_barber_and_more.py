# Generated by Django 4.2.6 on 2023-10-17 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0004_workingday_reserved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='barber',
        ),
        migrations.AddField(
            model_name='workingday',
            name='barber',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='workingday',
            unique_together={('date', 'time_slot')},
        ),
    ]
