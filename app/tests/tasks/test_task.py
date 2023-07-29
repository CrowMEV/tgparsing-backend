import pytest
from server import app
from settings import config


class TestTask:
    task_download_url: str = app.url_path_for(config.TASK_DOWNLOAD)
    task_delete_url: str = app.url_path_for(config.TASK_DELETE)

    download_data = [
        # wrong data
        ("", None, 422),
        ("test", None, 404),
        # correct data
        ("new_task", pytest.lazy_fixture("create_file"), 200),  # type: ignore
    ]

    @pytest.mark.parametrize("task_name,file_url,code", download_data)
    async def test_download_task(
        self,
        async_client,
        user_login,
        task_name,
        file_url,  # pylint: disable=W0613
        code,
    ):
        response = await async_client.get(
            self.task_download_url,
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
    async def test_delete_task(
        self, async_client, user_login, task_name, code
    ):
        response = await async_client.delete(
            self.task_delete_url,
            params={"task_name": task_name},
        )
        assert response.status_code == code
