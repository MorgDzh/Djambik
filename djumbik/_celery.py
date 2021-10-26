import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djumbik.settings')

app = Celery('djumbik.settings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
