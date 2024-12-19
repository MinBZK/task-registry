import logging
import os
from enum import StrEnum
from typing import Any

import yaml
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class TaskType(StrEnum):
    INSTRUMENTS = "instruments"
    REQUIREMENTS = "requirements"
    MEASURES = "measures"


class Link(BaseModel):
    self: str


class FileInfo(BaseModel):
    type: str
    size: int
    name: str
    path: str
    urn: str
    download_url: str
    links: Link


class Index(BaseModel):
    type: str = Field(examples=["dir"])
    size: int = Field(examples=[0])
    name: str = Field(examples=["task_collection_name"])
    path: str = Field(examples=["task_collection_path"])
    download_url: str = Field(examples=["https://task-registry.apps.digilab.network/task_collection"])
    links: Link = Field(examples=[{"self": "https://task-registry.apps.digilab.network"}])
    entries: list[FileInfo] = Field(
        examples=[
            {
                "type": "file",
                "size": 1024,
                "name": "task_name.yaml",
                "path": "task_collection_path/task_name.yaml",
                "urn": "urn:nl:aivt:tr:xx:xx",
                "download_url": "https://task-registry.apps.digilab.network/task_collection/urn/urn:nl:aivt:tr:aiia:1.0",
                "links": {
                    "self": "https://task-registry.apps.digilab.network/task_collection/urn/urn:nl:aivt:tr:aiia:1.0"
                },
            }
        ]
    )


class CachedRegistry:
    def __init__(self) -> None:
        self.index_cache: dict[TaskType, Index] = {}
        self.tasks_cache: dict[tuple[str, TaskType], Any] = {}

    def add_tasks(self, tasks: TaskType) -> None:
        index = generate_index(tasks)
        self.index_cache[tasks] = index

        for task in index.entries:
            try:
                with open(task.path) as f:
                    self.tasks_cache[(task.urn, tasks)] = yaml.safe_load(f)
            except FileNotFoundError:
                logger.exception(f"Task file with path {task.path} not found.")  # pragma: no cover
            except yaml.YAMLError:
                logger.exception(f"Task file with path {task.path} could not be parsed.")  # pragma: no cover

    def get_tasks_index(self, tasks: TaskType) -> Index:
        return self.index_cache[tasks]

    def get_task(self, urn: str, tasks: TaskType) -> dict[str, Any]:
        return self.tasks_cache[(urn, tasks)]

    def has_urn(self, urn: str, tasks: TaskType) -> bool:
        return (urn, tasks) in self.tasks_cache


def generate_index(
    tasks: TaskType,
    base_url: str = "https://task-registry.apps.digilab.network",
) -> Index:
    tasks_url = f"{base_url}/{tasks}"
    entries: list[FileInfo] = []

    for root, _, files in os.walk(tasks):
        for file in files:
            if file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                relative_path = file_path.replace("\\", "/")
                with open(file_path) as f:
                    task = yaml.safe_load(f)
                    task_url = f"{tasks_url}/urn/{task['urn']}"
                    file_info = FileInfo(
                        type="file",
                        size=os.path.getsize(file_path),
                        name=file,
                        path=relative_path,
                        urn=task["urn"],
                        download_url=task_url,
                        links=Link(self=task_url),
                    )
                    entries.append(file_info)

    return Index(
        type="dir",
        size=0,
        name=tasks.value,
        path=tasks.value,
        download_url=tasks_url,
        links=Link(self=tasks_url),
        entries=entries,
    )
