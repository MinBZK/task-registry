import logging
from unittest.mock import mock_open, patch

from task_registry import data
from tests.conftest import MOCK_TASK

logger = logging.getLogger(__name__)


def test_generate_index() -> None:
    filesize = 100
    dir = "/tasks"
    filename = "task_1.yaml"
    base_url = "https://ourapi.nl"
    task = data.TaskType.INSTRUMENTS

    with (
        patch("os.walk") as mock_walk,
        patch("os.path.getsize") as mock_getsize,
        patch("builtins.open", mock_open(read_data=f"{MOCK_TASK}")),
    ):
        mock_walk.return_value = [(dir, [], [filename])]
        mock_getsize.return_value = filesize

        index = data.generate_index(task, f"{base_url}")

        expected_index = data.Index(
            type="dir",
            size=0,
            name=task.value,
            path=task.value,
            download_url=f"{base_url}/instruments",
            links=data.Link(self=f"{base_url}/instruments"),
            entries=[
                data.FileInfo(
                    type="file",
                    size=filesize,
                    name=filename,
                    path=f"{dir}/{filename}",
                    urn=MOCK_TASK["urn"],
                    download_url=f'{base_url}/instruments/urn/{MOCK_TASK["urn"]}',
                    links=data.Link(self=f'{base_url}/instruments/urn/{MOCK_TASK["urn"]}'),
                )
            ],
        )

        assert index == expected_index
