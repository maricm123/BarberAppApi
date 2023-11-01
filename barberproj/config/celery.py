#celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.enable_utc = False

app.conf.update(timezone = 'Europe/Belgrade')

app.autodiscover_tasks()