from fastapi import Response, status
from fastapi.responses import JSONResponse
from fastapi_users.authentication import CookieTransport


class AppCookieTransport(CookieTransport):
    async def get_login_response(
        self, token: str, user_data: dict = None
    ) -> Response:
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content=user_data
        )
        return self._set_login_cookie(response, token)

    async def get_logout_response(self) -> Response:
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"status": "success"}
        )
        return self._set_logout_cookie(response)


cookie_transport = AppCookieTransport(
    cookie_name="tg_parsing", cookie_max_age=3600, cookie_secure=False
)
