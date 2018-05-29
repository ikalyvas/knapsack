import os
import sys

from celery import Celery
from multiprocessing import Process

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knap.settings')

app = Celery('knapsack')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
