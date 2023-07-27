import asyncio

from services.telegram.bot_server.utils import do_parsing
from utils.celery.celery_app import celery_app


@celery_app.task
def start_parsing(
    parsing_task: str,
    data: dict,
):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        do_parsing(
            parsing_task=parsing_task,
            data=data,
        )
    )
