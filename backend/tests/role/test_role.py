# import pytest
#
# from server import app
# from settings import config
#
#
# class TestRole:
#     add_url: str = app.url_path_for(config.ROLE_ADD)
#
#     register_data = [
#         # correct data
#         ("NewRole", 201),
#     ]
#
#     @pytest.mark.parametrize("name,code", register_data)
#     async def test_role_add(self, async_client, admin_login, name, code):
#         response = await async_client.post(
#             self.add_url,
#             json={
#                 "name": name,
#             },
#         )
#
#         assert response.status_code == code
