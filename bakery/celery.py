import os

from celery.schedules import crontab

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery.settings')

app = Celery('bakery')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {

    'delete_tokens': {
        'task': 'authentication.tasks.delete_tokens',
        'schedule': crontab(0, 0, day_of_month='2-30/3'),
        'args': (),
    }
}
