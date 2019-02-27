from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

from Shops.settings import CELERY_CONFIGURATION

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Shops.settings')


app = Celery()
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(**CELERY_CONFIGURATION)
app.autodiscover_tasks()
