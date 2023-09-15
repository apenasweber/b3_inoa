import os
from datetime import timedelta

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "b3_inoa.settings")

app = Celery("b3_inoa")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "collect-prices-every-30-minutes": {
        "task": "trading.tasks.task_collect_prices",
        "schedule": timedelta(minutes=30),
        "args": (),
    },
}
