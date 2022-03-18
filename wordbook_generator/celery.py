import os

from celery import Celery
from celery.signals import after_setup_task_logger


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wordbook_generator.settings.development')

app = Celery('wordbook_generator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
