import pytest


class TestUser:
    prefix: str = '/user'

    register_data = [
        # wrong email
        ('@mail.ru', 'Igor', 'Pupkin', '123', 422),
        ('1@', 'Igor', 'Pupkin', '123', 422),
        ('1@mail', 'Igor', 'Pupkin', '123', 422),
        ('1@mail.', 'Igor', 'Pupkin', '123', 422),
        ('1@.ru', 'Igor', 'Pupkin', '123', 422),

        # wrong firstname
        ('1@mail.ru', '', 'Pupkin', '123', 422),
        ('1@mail.ru', ' ', 'Pupkin', '123', 422),
        ('1@mail.ru', ' Igor', 'Pupkin', '123', 422),
        ('1@mail.ru', '&Igor', 'Pupkin', '123', 422),
        ('1@mail.ru', '1Igor', 'Pupkin', '123', 422),
        ('1@mail.ru', 'Igor1', 'Pupkin', '123', 422),
        ('1@mail.ru', 'Igor ', 'Pupkin', '123', 422),
        ('1@mail.ru', 'Igor%', 'Pupkin', '123', 422),

        # wrong lastname
        ('1@mail.ru', 'Igor', '', '123', 422),
        ('1@mail.ru', 'Igor', ' ', '123', 422),
        ('1@mail.ru', 'Igor', ' Pupkin', '123', 422),
        ('1@mail.ru', 'Igor', '1Pupkin', '123', 422),
        ('1@mail.ru', 'Igor', '%Pupkin', '123', 422),
        ('1@mail.ru', 'Igor', 'Pupkin ', '123', 422),
        ('1@mail.ru', 'Igor', 'Pupkin1', '123', 422),
        ('1@mail.ru', 'Igor', 'Pupkin%', '123', 422),

        # wrong password
        ('1@mail.ru', 'Igor', 'Pupkin', '', 422),
        ('1@mail.ru', 'Igor', 'Pupkin', '1michail#', 422),
        ('1@mail.ru', 'Igor', 'Pupkin', 'Michail#', 422),
        ('1@mail.ru', 'Igor', 'Pupkin', '1Michail', 422),
        ('1@mail.ru', 'Igor', 'Pupkin', '1michail#', 422),

        # correct data
        ('1@mail.ru', 'Igor', 'Pupkin', '1Michail#', 201),
    ]

    @pytest.mark.parametrize('email,name,surname,password,code', register_data)
    async def test_user_register(
            self, async_client, email, name, surname, password, code
    ):
        response = await async_client.post(
            f"{self.prefix}/register",
            json={
                "email": email,
                "firstname": name,
                "lastname": surname,
                "password": password
            }
        )

        assert response.status_code == code

    login_data = [
        # wrong data
        ('2@mail.ru', '1Michail#', 400),
        ('1@mail.ru', '2Michail#', 400),

        # correct data
        ('1@mail.ru', '1Michail#', 200),
    ]

    @pytest.mark.parametrize('email,password,code', login_data)
    async def test_user_login(self, async_client, email, password, code):
        response = await async_client.post(
            f"{self.prefix}/login",
            json={
                "email": email,
                "password": password
            }
        )

        assert response.status_code == code

    patch_data = [
        # wrong firstname
        (' ', 'Pupkin', '123', 422),
        (' Igor', 'Pupkin', '123', 422),
        ('&Igor', 'Pupkin', '123', 422),
        ('1Igor', 'Pupkin', '123', 422),
        ('Igor1', 'Pupkin', '123', 422),
        ('Igor ', 'Pupkin', '123', 422),
        ('Igor%', 'Pupkin', '123', 422),

        # wrong lastname
        ('Igor', ' ', '123', 422),
        ('Igor', ' Pupkin', '123', 422),
        ('Igor', '1Pupkin', '123', 422),
        ('Igor', '%Pupkin', '123', 422),
        ('Igor', 'Pupkin ', '123', 422),
        ('Igor', 'Pupkin1', '123', 422),
        ('Igor', 'Pupkin%', '123', 422),

        # wrong password
        ('Igor', 'Pupkin', '1michail#', 422),
        ('Igor', 'Pupkin', 'Michail#', 422),
        ('Igor', 'Pupkin', '1Michail', 422),
        ('Igor', 'Pupkin', '1michail#', 422),

        # correct data
        ('Vasya', '', '', 200),
        ('', 'Gordeev', '', 200),
        ('', '', 'HEro2023#', 200),
        ('Masha', 'Zacharova', 'sAlenow2023#', 200),
    ]

    @pytest.mark.parametrize('name,surname,password,code', patch_data)
    async def test_user_patch(
            self, async_client, name, surname, password, code
    ):
        params = {
            "firstname": name,
            "lastname": surname,
            "password": password
        }
        params = {key: value for key, value in params.items() if value}
        response = await async_client.patch(
            f"{self.prefix}/patch",
            data=params
        )

        assert response.status_code == code

    logout_data = [
        200,
        401,
    ]

    @pytest.mark.parametrize('code', logout_data)
    async def test_user_logout(self, async_client, code):
        response = await async_client.post(
            f"{self.prefix}/logout",
        )

        assert response.status_code == code
