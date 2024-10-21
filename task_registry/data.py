import logging
import os
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


def get_file_size(file_path: str) -> int:
    return os.path.getsize(file_path)  # pragma: no cover


def create_urn_mappper(entries: list[dict[str, Any]]) -> dict[str, Any]:
    urn_mapper: dict[str, Any] = {}
    for instrument in entries:
        path = Path(instrument["path"])
        try:
            with open(str(path)) as f:
                urn_mapper[instrument["urn"]] = yaml.safe_load(f)
        except FileNotFoundError:
            logger.exception(f"Instrument file with path {path} not found.")  # pragma: no cover

        except yaml.YAMLError:
            logger.exception(f"Instrument file with path {path} could not be parsed.")  # pragma: no cover

    return urn_mapper


def generate_index(
    base_url: str = "https://task-registry.apps.digilab.network",
    directory: str = "instruments",
) -> dict[str, Any]:
    index: dict[str, Any] = {
        "type": "dir",
        "size": 0,
        "name": directory,
        "path": directory,
        "download_url": f"{base_url}/instruments",
        "_links": {
            "self": f"{base_url}/instruments",
        },
        "entries": [],
    }

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                relative_path = file_path.replace("\\", "/")
                with open(file_path) as f:
                    instrument = yaml.safe_load(f)
                    file_info = {
                        "type": "file",
                        "size": get_file_size(file_path),
                        "name": file,
                        "path": relative_path,
                        "urn": instrument["urn"],
                        "download_url": f"{base_url}/urns/?urn={instrument['urn']}",
                        "_links": {
                            "self": f"{base_url}/urns/?urn={instrument['urn']}",
                        },
                    }
                    index["entries"].append(file_info)

    return index
