from fastapi import APIRouter

from services.payment import views
from settings import config

payment_router = APIRouter(prefix="/payment", tags=["Payment"])

payment_router.add_api_route(
    path="/",
    endpoint=views.get_payment_link,
    methods=["POST"],
    name=config.PAYMENT_ADD,
)
