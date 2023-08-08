from settings import config


broker_url = f"redis://{config.BROKER_HOST}:{config.BROKER_PORT}"

broker_connection_retry_on_startup = True  # pylint: disable=C0103
include = [
    "services.telegram.bot_server.orders",
    "services.tariff.tasks",
]
