from celery import Celery  # type: ignore
from celery.schedules import crontab  # type: ignore
from settings import config
from utils.celery import celeryconfig


celery_app = Celery(config.APP_NAME)
celery_app.config_from_object(celeryconfig)


celery_app.conf.beat_schedule = {
    "daily-options-reset": {
        "task": "services.tariff.tasks.reset_options_daily",
        "schedule": crontab(minute="0", hour="0"),
    },
    "daily-subs-reset": {
        "task": "services.tariff.tasks.tariff_active_debit_daily",
        "schedule": crontab(minute="0", hour="0"),
    },
}
