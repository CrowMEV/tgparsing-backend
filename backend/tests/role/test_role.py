#
#
#
# class TestRole:
#     prefix: str = "/roles"
#
#     register_data = [
#         # correct data
#         ("NewRole", 201),
#     ]
#
#     @pytest.mark.parametrize("name,code", register_data)
#     async def test_user_register(self, async_client, name, code):
#         response = await async_client.post(
#             f"{self.prefix}/",
#             json={
#                 "name": name,
#             },
#         )
#
#         assert response.status_code == code
#
