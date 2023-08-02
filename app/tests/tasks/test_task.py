import pytest
from server import app
from settings import config


class TestTask:
    admin_get_tasks_url: str = app.url_path_for(config.TASK_GET_ALL)
    user_get_tasks_url: str = app.url_path_for(config.TASK_ME_GET_ALL)
    user_download_url: str = app.url_path_for(config.TASK_ME_DOWNLOAD_FILE)
    user_delete_url: str = app.url_path_for(config.TASK_ME_DELETE)

    async def test_user_get_tasks(self, async_client, user_login):
        response = await async_client.get(
            self.user_get_tasks_url,
        )
        assert response.status_code == 200

    async def test_user_get_all_db_tasks(self, async_client, user_login):
        response = await async_client.get(
            self.admin_get_tasks_url,
        )
        assert response.status_code == 403

    async def test_admin_get_user_tasks(self, async_client, superuser_login):
        response = await async_client.get(
            self.user_get_tasks_url,
        )
        assert response.status_code == 200

    async def test_get_tasks(self, async_client, superuser_login):
        response = await async_client.get(
            self.admin_get_tasks_url,
        )
        assert response.status_code == 200

    download_data = [
        # wrong data
        ("", None, 422),
        ("test", None, 404),
        # correct data
        ("new_task", pytest.lazy_fixture("create_file"), 200),  # type: ignore
    ]

    @pytest.mark.parametrize("task_name,file_url,code", download_data)
    async def test_user_download_file(
        self,
        async_client,
        user_login,
        task_name,
        file_url,  # pylint: disable=W0613
        code,
    ):
        response = await async_client.get(
            self.user_download_url,
            params={"task_name": task_name},
        )
        assert response.status_code == code

    delete_data = [
        # wrong data
        ("", 422),
        ("test", 404),
        # correct data
        ("new_task", 200),
    ]

    @pytest.mark.parametrize("task_name,code", delete_data)
    async def test_user_delete_task(
        self, async_client, user_login, task_name, code
    ):
        response = await async_client.delete(
            self.user_delete_url,
            params={"task_name": task_name},
        )
        assert response.status_code == code
