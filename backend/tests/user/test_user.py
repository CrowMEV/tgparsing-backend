import pytest

from server import app
from settings import config


class TestUser:
    register_url: str = app.url_path_for(config.USER_REGISTER)
    login_url: str = app.url_path_for(config.USER_LOGIN)
    logout_url: str = app.url_path_for(config.USER_LOGOUT)
    patch_url: str = app.url_path_for(config.USER_PATCH)

    register_data = [
        # wrong email
        ("@mail.ru", "123", 422),
        ("1@", "123", 422),
        ("1@mail", "123", 422),
        ("1@mail.", "123", 422),
        ("1@.ru", "123", 422),
        # wrong password
        ("1@mail.ru", "", 422),
        ("1@mail.ru", "1michail#", 422),
        ("1@mail.ru", "Michail#", 422),
        ("1@mail.ru", "1Michail", 422),
        ("1@mail.ru", "1michail#", 422),
        # correct data
        ("1@mail.ru", "1Michail#", 201),
    ]

    @pytest.mark.parametrize("email,password,code", register_data)
    async def test_user_register(self, async_client, email, password, code):
        response = await async_client.post(
            self.register_url,
            json={"email": email, "password": password},
        )

        assert response.status_code == code

    login_data = [
        # wrong data
        ("2@mail.ru", "1Michail#", 400),
        ("1@mail.ru", "2Michail#", 400),
        # correct data
        ("1@mail.ru", "1Michail#", 200),
    ]

    @pytest.mark.parametrize("email,password,code", login_data)
    async def test_user_login(self, async_client, email, password, code):
        response = await async_client.post(
            self.login_url, json={"email": email, "password": password}
        )

        assert response.status_code == code

    patch_data = [
        # wrong firstname
        (" ", "Pupkin", "123", "+2904242", "igor@pupkin.com", 422),
        (" Igor", "Pupkin", "123", "+2904242", "igor@pupkin.com", 422),
        ("&Igor", "Pupkin", "123", "+2904242", "igor@pupkin.com", 422),
        ("1Igor", "Pupkin", "123", "+2904242", "igor@pupkin.com", 422),
        ("Igor1", "Pupkin", "123", "+2904242", "igor@pupkin.com", 422),
        ("Igor ", "Pupkin", "123", "+2904242", "igor@pupkin.com", 422),
        ("Igor%", "Pupkin", "123", "+2904242", "igor@pupkin.com", 422),
        # wrong lastname
        ("Igor", " ", "123", "+2904242", "igor@pupkin.com", 422),
        ("Igor", " Pupkin", "123", "+2904242", "igor@pupkin.com", 422),
        ("Igor", "1Pupkin", "123", "+2904242", "igor@pupkin.com", 422),
        ("Igor", "%Pupkin", "123", "+2904242", "igor@pupkin.com", 422),
        ("Igor", "Pupkin ", "123", "+2904242", "igor@pupkin.com", 422),
        ("Igor", "Pupkin1", "123", "+2904242", "igor@pupkin.com", 422),
        ("Igor", "Pupkin%", "123", "+2904242", "igor@pupkin.com", 422),
        # wrong password
        ("Igor", "Pupkin", "1michail#", "+2904242", "igor@pupkin.com", 422),
        ("Igor", "Pupkin", "Michail#", "+2904242", "igor@pupkin.com", 422),
        ("Igor", "Pupkin", "1Michail", "+2904242", "igor@pupkin.com", 422),
        ("Igor", "Pupkin", "1michail#", "+2904242", "igor@pupkin.com", 422),
        # wrong phone_number
        ("Igor", "Pupkin", "123", "lalala", "igor@pupkin.com", 422),
        ("Igor", "Pupkin", "123", "89997775544", "igor@pupkin.com", 422),
        (
            "Igor", "Pupkin", "123",
            "+8888 8888 77775566", "igor@pupkin.com", 422
        ),
        ("Igor", "Pupkin", "123", "+341234", "igor@pupkin.com", 422),
        ("Igor", "Pupkin", "123", " ", "igor@pupkin.com", 422),
        # wrong email
        ("Igor", "Pupkin", "123", "+2904242", "igor#pupkin.com", 422),
        ("Igor", "Pupkin", "123", "+2904242", "igorpupkin.com", 422),
        ("Igor", "Pupkin", "123", "+2904242", "igor123pupkin.com", 422),
        ("Igor", "Pupkin", "123", "+2904242", "123%", 422),
        # correct data
        ("Vasya", "", "", "", "", 200),
        ("", "Gordeev", "", "", "", 200),
        ("", "", "HEro2023#", "", "", 200),
        ("", "", "", "+37 (787) 5675656", "", 200),
        (
            "Masha", "Zacharova", "sAlenow2023#",
            "+79998886655", "igor@pupkin.com", 200
        ),
    ]

    @pytest.mark.parametrize(
        "name,surname,password,phone_number,email,code", patch_data
    )
    async def test_user_patch(
        self, async_client, name, surname, password, phone_number, email, code
    ):
        params = {
            "firstname": name, "lastname": surname,
            "password": password, "phone_number": phone_number,
            "email": email
        }
        params = {key: value for key, value in params.items() if value}
        response = await async_client.patch(self.patch_url, data=params)

        assert response.status_code == code

    logout_data = [
        200,
        401,
    ]

    @pytest.mark.parametrize("code", logout_data)
    async def test_user_logout(self, async_client, code):
        response = await async_client.post(
            self.logout_url,
        )

        assert response.status_code == code
