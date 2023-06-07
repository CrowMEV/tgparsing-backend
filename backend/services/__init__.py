# from sqlalchemy.orm import declarative_base
# #
# #
# Base = declarative_base()
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# def get_base():
#     import services.role.models as role_models
#     import services.tariff.models as tariff_models
#     import services.user.models as user_models
#     import services.payment.models as payment_models
#
#     return BaseModel
#
#
# Base = get_base()
