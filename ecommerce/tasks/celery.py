from __future__ import absolute_import, unicode_literals

from celery import Celery

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

app = Celery('ecommerce')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.timezone = 'America/Guayaquil'

app.autodiscover_tasks()