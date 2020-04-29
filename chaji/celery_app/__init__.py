import os
from datetime import timedelta

from celery.schedules import crontab
from django.conf import settings
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chaji.settings")

app = Celery('tasks', )

app.config_from_object('celery_app.celeryconfig')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



app.conf.update(
    CELERYBEAT_SCHEDULE={
        'sum-task': {
            'task': 'celery_app.tasks.add',
            'schedule': timedelta(seconds=20),
            'args': (5, 3)
        },
        'send-email': {
            'task': 'info.tasks.send_email',
            'schedule': crontab(minute='*/2'),
            'args': ()
        }
    }
)

