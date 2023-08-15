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
        ({"email": "@mail.ru", "password": "123"}, 422),
        ({"email": "1@", "password": "123"}, 422),
        ({"email": "1@mail", "password": "123"}, 422),
        ({"email": "1@mail.", "password": "123"}, 422),
        ({"email": "1@.ru", "password": "123"}, 422),
        # wrong password
        ({"email": "1@mail.ru", "password": ""}, 422),
        ({"email": "1@mail.ru", "password": "1michail#"}, 422),
        ({"email": "1@mail.ru", "password": "Michail#"}, 422),
        ({"email": "1@mail.ru", "password": "1Michail"}, 422),
        ({"email": "1@mail.ru", "password": "1michail#"}, 422),
        # correct data
        ({"email": "1@mail.ru", "password": "1Michail#"}, 201),
    ]

    @pytest.mark.parametrize("data,code", register_data)
    async def test_user_register(self, async_client, data, code):
        response = await async_client.post(
            self.register_url,
            json=data,
        )

        assert response.status_code == code

    login_data = [
        # wrong data
        ({"email": "2@mail.ru", "password": "1Michail#"}, 400),
        ({"email": "1@mail.ru", "password": "2Michail#"}, 400),
        # correct data
        ({"email": "1@mail.ru", "password": "1Michail#"}, 200),
    ]

    @pytest.mark.parametrize("data,code", login_data)
    async def test_user_login(self, async_client, data, code):
        response = await async_client.post(self.login_url, json=data)

        assert response.status_code == code

    patch_data = [
        # wrong firstname
        ({"firstname": " "}, 422),
        ({"firstname": " Igor"}, 422),
        ({"firstname": "&Igor"}, 422),
        ({"firstname": "1Igor"}, 422),
        ({"firstname": "Igor1"}, 422),
        ({"firstname": "Igor "}, 422),
        ({"firstname": "Igor-"}, 422),
        ({"firstname": "Igor%"}, 422),
        ({"firstname": "igor"}, 422),
        # wrong lastname
        ({"lastname": " "}, 422),
        ({"lastname": " Pupkin"}, 422),
        ({"lastname": "1Pupkin"}, 422),
        ({"lastname": "%Pupkin"}, 422),
        ({"lastname": "Pupkin "}, 422),
        ({"lastname": "Pupkin1"}, 422),
        ({"lastname": "Pupkin%"}, 422),
        ({"lastname": "Pupkin-"}, 422),
        ({"lastname": "pupkin"}, 422),
        # wrong password
        ({"password": "1michail#"}, 422),
        ({"password": "Michail#"}, 422),
        ({"password": "1Michail"}, 422),
        ({"password": "1michail#"}, 422),
        # wrong phone_number
        ({"phone_number": "lalala"}, 422),
        ({"phone_number": "89997775544"}, 422),
        ({"phone_number": "+8888 8888 77775566"}, 422),
        ({"phone_number": "+341234"}, 422),
        ({"phone_number": " "}, 422),
        # wrong email
        ({"email": "igor#pupkin.com"}, 422),
        ({"email": "igorpupkin.com"}, 422),
        ({"email": "igor123pupkin.com"}, 422),
        ({"email": "123%"}, 422),
        # correct data
        ({"firstname": "Vasya"}, 200),
        ({"lastname": "Gordeev"}, 200),
        ({"password": "HEro2023#"}, 200),
        ({"phone_number": "+37(787)5675656"}, 200),
        (
            {
                "firstname": "Masha",
                "lastname": "Zacharova",
                "password": "sAlenow2023#",
                "phone_number": "+79998886655",
                "email": "igor@pupkin.com",
            },
            200,
        ),
    ]

    @pytest.mark.parametrize("data,code", patch_data)
    async def test_user_patch(self, async_client, data, code):
        response = await async_client.patch(self.patch_url, data=data)

        assert response.status_code == code

    async def test_user_patch_by_user(self, async_client, user_login):
        url = app.url_path_for(config.USER_PATCH_BY_ADMIN, id_row=1)
        response = await async_client.patch(url)

        assert response.status_code == 403

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

    superuser_patch_data = [
        # wrong id
        (" ", {}, 422),
        ("lala", {}, 422),
        (99999999, {}, 400),
        # wrong firstname
        (1, {"firstname": " "}, 422),
        (1, {"firstname": " Igor"}, 422),
        (1, {"firstname": "&Igor"}, 422),
        (1, {"firstname": "1Igor"}, 422),
        (1, {"firstname": "Igor1"}, 422),
        (1, {"firstname": "Igor "}, 422),
        (1, {"firstname": "Igor%"}, 422),
        # wrong lastname
        (1, {"firstname": "123"}, 422),
        (1, {"firstname": " Pupkin"}, 422),
        (1, {"firstname": "1Pupkin"}, 422),
        (1, {"firstname": "%Pupkin"}, 422),
        (1, {"firstname": "Pupkin "}, 422),
        (1, {"firstname": "Pupkin1"}, 422),
        (1, {"firstname": "Pupkin%"}, 422),
        # wrong password
        (1, {"password": "1michail#"}, 422),
        (1, {"password": "Michail#"}, 422),
        (1, {"password": "1Michail"}, 422),
        (1, {"password": "1michail#"}, 422),
        # wrong phone_number
        (1, {"phone_number": "lalala"}, 422),
        (1, {"phone_number": "89997775544"}, 422),
        (1, {"phone_number": "+8888 8888 77775566"}, 422),
        (1, {"phone_number": "+341234"}, 422),
        ("1", {"phone_number": " "}, 422),
        # wrong email
        (1, {"email": "igor#pupkin.com"}, 422),
        (1, {"email": "igorpupkin.com"}, 422),
        (1, {"email": "igor123pupkin.com"}, 422),
        ("1", {"email": "123%"}, 422),
        # wrong param
        (1, {"is_staff": True}, 400),
        # wrong role
        (1, {"role": "loser"}, 422),
        # can't update superuser
        ("2", {"lastname": "Gor"}, 403),
        # correct data
        (3, {"firstname": "Valera"}, 200),
        (3, {"lastname": "Gor"}, 200),
        (3, {"password": "HEro202333#"}, 200),
        (3, {"phone_number": "+38(787)5675659"}, 200),
        (3, {"email": "igor123@user.com"}, 200),
        (3, {"role": "hr"}, 200),
        (
            3,
            {
                "firstname": "Dasha",
                "lastname": "Zecharova",
                "password": "sAlenowS2023#",
                "phone_number": "+79998886600",
                "email": "dasha@pukin.com",
                "role": "accountant",
            },
            200,
        ),
        # # Check double values. This test depends on the previous entity
        (
            3,
            {"phone_number": "+79998886600"},
            400,
        ),
        (
            3,
            {"email": "dasha@pukin.com"},
            400,
        ),
    ]

    @pytest.mark.parametrize(
        "id_row,data,code",
        superuser_patch_data,
    )
    async def test_user_patch_by_superuser(
        self, async_client, superuser_login, id_row, data, code
    ):
        url = app.url_path_for(config.USER_PATCH_BY_ADMIN, id_row=id_row)
        response = await async_client.patch(url, data=data)

        assert response.status_code == code

    admin_patch_data = [
        # wrong permission
        ("2", {"role_name": "superuser"}, 403),
        # correct data
        ("3", {"is_banned": False}, 200),
        ("3", {"is_banned": True}, 200),
        ("3", {"role": "hr"}, 200),
        (
            "3",
            {
                "firstname": "Dasha",
                "lastname": "Zecharova",
                "password": "sAlenowS2023#",
                "phone_number": "+79998886601",
                "email": "admin@admin.com",
                "role": "user",
            },
            200,
        ),
    ]

    @pytest.mark.parametrize(
        "id_row,data,code",
        admin_patch_data,
    )
    async def test_user_patch_by_admin(
        self, async_client, admin_login, id_row, data, code
    ):
        url = app.url_path_for(config.USER_PATCH_BY_ADMIN, id_row=id_row)
        response = await async_client.patch(url, data=data)

        assert response.status_code == code
