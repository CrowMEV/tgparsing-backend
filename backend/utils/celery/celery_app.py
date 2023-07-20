from celery import Celery  # type: ignore

from settings import config
from utils.celery import celeryconfig


# from celery.schedules import crontab


celery_app = Celery(config.APP_NAME)
celery_app.config_from_object(celeryconfig)

# celery_app.autodiscover_tasks(packages=["tasks.subscribes"])
#
# celery_app.conf.beat_schedule = {
#     "daily-subs-reset": {
#         "task": "tasks.subscribes.tasks.reset_options_daily",
#         "schedule": crontab(minute="0", hour="0"),
#     }
# }
