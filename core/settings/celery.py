from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.develop')

app = Celery('Afsona')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
