import pytest
from server import app
from settings import config


class TestRole:
    get_all_roles: str = app.url_path_for(config.ROLE_GET_ALL)
    patch_role: str = app.url_path_for(config.ROLE_PATCH)

    async def test_get_roles_by_admin(self, async_client, admin_login):
        response = await async_client.get(self.get_all_roles)

        assert response.status_code == 200

    async def test_get_roles_by_user(self, async_client, user_login):
        response = await async_client.get(self.get_all_roles)

        assert response.status_code == 403

    admin_change_data = [
        # wrong data
        ({"is_active": True}, 422),
        ({"staff_action": ["delete"]}, 422),
        ({"payment_action": ["delete"]}, 422),
        # correct data
        ({"name": "user", "is_active": False}, 200),
        ({"name": "user", "payment_action": ["delete"]}, 200),
        (
            {
                "name": "user",
                "is_active": True,
                "staff_action": ["delete"],
            },
            200,
        ),
    ]

    @pytest.mark.parametrize("data,code", admin_change_data)
    async def test_change_role_by_admin(
        self, async_client, admin_login, data, code
    ):
        response = await async_client.patch(self.patch_role, json=data)

        assert response.status_code == code

    user_change_data = [
        # correct data
        ({"name": "user", "is_active": True}, 403),
    ]

    @pytest.mark.parametrize("data,code", user_change_data)
    async def test_change_role_by_user(
        self, async_client, user_login, data, code
    ):
        response = await async_client.patch(self.patch_role, json=data)

        assert response.status_code == code
