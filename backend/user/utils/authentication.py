from fastapi import Response, status
from fastapi_users import models
from fastapi_users.authentication import AuthenticationBackend
import fastapi_users.authentication.transport as fu_tr
import fastapi_users.authentication.strategy as fu_str

from user.schemas import UserRead
from user.utils.cookie_transport import cookie_transport, AppCookieTransport
from user.utils.strategy import get_jwt_strategy


class AppAuthenticationBackend(AuthenticationBackend):
    transport: AppCookieTransport

    async def login(
        self, strategy: fu_str.Strategy[models.UP, models.ID], user: models.UP
    ) -> Response:
        token = await strategy.write_token(user)
        user = UserRead(**user.__dict__).__dict__
        return await self.transport.get_login_response(token, user)

    async def logout(
        self,
        strategy: fu_str.Strategy[models.UP, models.ID],
        user: models.UP,
        token: str,
    ) -> Response:
        try:
            await strategy.destroy_token(token, user)
        except fu_str.StrategyDestroyNotSupportedError:
            pass

        try:
            response = await self.transport.get_logout_response()
        except fu_tr.TransportLogoutNotSupportedError:
            response = Response(status_code=status.HTTP_204_NO_CONTENT)

        return response


auth_backend = AppAuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
