from datetime import datetime, timedelta

import services.tariff.db_handlers as tariff_db_hand
import services.user.db_handlers as user_db_hand
from database.db_sync import Session
from utils.celery.celery_app import celery_app


@celery_app.task
def reset_options_daily():
    with Session() as session:
        tariffs = tariff_db_hand.get_tariffs_sync(session)
    tariff_db_hand.update_subscribe_options_sync(session, tariffs)


@celery_app.task
def tariff_active_debit_daily():
    with Session() as session:
        subscribes = tariff_db_hand.get_subscribes_sync(session)
        for subscribe in subscribes:
            if subscribe.end_date > datetime.utcnow():
                continue
            if subscribe.auto_debit:
                if subscribe.user.balance < subscribe.tariff.price:
                    tariff_db_hand.update_user_subscribe_sync(
                        session, subscribe.user_id, {"active": False}
                    )
                    continue
                user_db_hand.update_user_sync(
                    session,
                    subscribe.user_id,
                    {
                        "balance": (
                            subscribe.user.balance - subscribe.tariff.price
                        ),
                    },
                )
                tariff_db_hand.update_user_subscribe_sync(
                    session,
                    subscribe.user_id,
                    {
                        "active": True,
                        "end_date": (
                            datetime.utcnow()
                            + timedelta(subscribe.tariff.limitation_days)
                        ),
                    },
                )
            else:
                tariff_db_hand.update_user_subscribe_sync(
                    session, subscribe.user_id, {"active": False}
                )
