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
            "Igor",
            "Pupkin",
            "123",
            "+8888 8888 77775566",
            "igor@pupkin.com",
            422,
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
        ("", "", "", "+37(787)5675656", "", 200),
        (
            "Masha",
            "Zacharova",
            "sAlenow2023#",
            "+79998886655",
            "igor@pupkin.com",
            200,
        ),
    ]

    @pytest.mark.parametrize(
        "name,surname,password,phone_number,email,code", patch_data
    )
    async def test_user_patch(
        self, async_client, name, surname, password, phone_number, email, code
    ):
        params = {
            "firstname": name,
            "lastname": surname,
            "password": password,
            "phone_number": phone_number,
            "email": email,
        }
        params = {key: value for key, value in params.items() if value}
        response = await async_client.patch(self.patch_url, params=params)

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
        (
            " ",
            "Igor",
            "Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "lala",
            "Igor",
            "Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "44",
            "Igor",
            "Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        # wrong firstname
        (
            "1",
            " ",
            "Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            " Igor",
            "Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "&Igor",
            "Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "1Igor",
            "Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor1",
            "Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor ",
            "Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor%",
            "Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        # wrong lastname
        ("1", "Igor", " ", "123", "+2904242", "igor@pupkin.com", "", "", 422),
        (
            "1",
            "Igor",
            " Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "1Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "%Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "Pupkin ",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "Pupkin1",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "Pupkin%",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        # wrong password
        (
            "1",
            "Igor",
            "Pupkin",
            "1michail#",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "Pupkin",
            "Michail#",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "Pupkin",
            "1Michail",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "Pupkin",
            "1michail#",
            "+2904242",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        # wrong phone_number
        (
            "1",
            "Igor",
            "Pupkin",
            "123",
            "lalala",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "Pupkin",
            "123",
            "89997775544",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "Pupkin",
            "123",
            "+8888 8888 77775566",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "Pupkin",
            "123",
            "+341234",
            "igor@pupkin.com",
            "",
            "",
            422,
        ),
        ("1", "Igor", "Pupkin", "123", " ", "igor@pupkin.com", "", "", 422),
        # wrong email
        (
            "1",
            "Igor",
            "Pupkin",
            "123",
            "+2904242",
            "igor#pupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "Pupkin",
            "123",
            "+2904242",
            "igorpupkin.com",
            "",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "Pupkin",
            "123",
            "+2904242",
            "igor123pupkin.com",
            "",
            "",
            422,
        ),
        ("1", "Igor", "Pupkin", "123", "+2904242", "123%", "", "", 422),
        # wrong is_staff
        (
            "1",
            "Igor",
            "Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "Igor",
            "",
            422,
        ),
        (
            "1",
            "Igor",
            "Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "123",
            "",
            422,
        ),
        # wrong role
        (
            "1",
            "Igor",
            "Pupkin",
            "123",
            "+2904242",
            "igor@pupkin.com",
            "True",
            "loser",
            422,
        ),
        # wrong permission
        ("1", "Valera", "", "", "", "", "", "", 403),
        ("2", "", "Gor", "", "", "", "", "", 403),
        # correct data
        ("3", "Valera", "", "", "", "", "", "", 200),
        ("3", "", "Gor", "", "", "", "", "", 200),
        ("3", "", "", "HEro202333#", "", "", "", "", 200),
        ("3", "", "", "", "+38(787)5675659", "", "", "", 200),
        ("3", "", "", "", "", "", "True", "", 200),
        ("3", "", "", "", "", "", "", "hr", 200),
        (
            "3",
            "Dasha",
            "Zecharova",
            "sAlenowS2023#",
            "+79998886600",
            "dasha@pukin.com",
            "False",
            "accountant",
            200,
        ),
    ]

    @pytest.mark.parametrize(
        "id_row,name,surname,password,phone_number,email,is_staff,role,code",
        superuser_patch_data,
    )
    async def test_user_patch_by_superuser(
        self,
        async_client,
        superuser_login,
        id_row,
        name,
        surname,
        password,
        phone_number,
        email,
        is_staff,
        role,
        code,
    ):
        params = {
            "firstname": name,
            "lastname": surname,
            "password": password,
            "phone_number": phone_number,
            "email": email,
            "is_staff": is_staff,
            "role": role,
        }
        params = {key: value for key, value in params.items() if value}
        url = app.url_path_for(config.USER_PATCH_BY_ADMIN, id_row=id_row)
        response = await async_client.patch(url, params=params)

        assert response.status_code == code

    admin_patch_data = {
        # wrong permission
        ("1", "Valera", "", "", "", "", "", "", "", 403),
        # correct data
        ("3", "", "", "", "", "", "False", "", "", 200),
        ("3", "", "", "", "", "", "", "False", "", 200),
        ("3", "", "", "", "", "", "", "", "hr", 200),
        (
            "3",
            "Dasha",
            "Zecharova",
            "sAlenowS2023#",
            "+79998886600",
            "dasha@pukin.com",
            "True",
            "",
            "user",
            200,
        ),
    }

    @pytest.mark.parametrize(
        "id_row,name,surname,password,phone,email,active,staff,role,code",
        admin_patch_data,
    )
    async def test_user_patch_by_admin(
        self,
        async_client,
        admin_login,
        id_row,
        name,
        surname,
        password,
        phone,
        email,
        active,
        staff,
        role,
        code,
    ):
        params = {
            "firstname": name,
            "lastname": surname,
            "password": password,
            "phone_number": phone,
            "email": email,
            "is_active": active,
            "is_staff": staff,
            "role": role,
        }
        params = {key: value for key, value in params.items() if value}
        url = app.url_path_for(config.USER_PATCH_BY_ADMIN, id_row=id_row)
        response = await async_client.patch(url, params=params)

        assert response.status_code == code
