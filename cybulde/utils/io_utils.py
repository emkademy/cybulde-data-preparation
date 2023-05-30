from typing import Any

import yaml

from fsspec import AbstractFileSystem, filesystem

GCS_PREFIX = "gs://"
GCS_FILE_SYSTEM_NAME = "gcs"
LOCAL_FILE_SYSTEM_NAME = "file"
TMP_FILE_PATH = "/tmp/"


def choose_file_file(path: str) -> AbstractFileSystem:
    return filesystem(GCS_FILE_SYSTEM_NAME) if path.startswith(GCS_PREFIX) else filesystem(LOCAL_FILE_SYSTEM_NAME)


def open_file(path: str, mode: str = "r") -> Any:
    file_system = choose_file_file(path)
    return file_system.open(path, mode)


def write_yaml_file(yaml_file_path: str, yaml_file_content: dict[Any, Any]) -> None:
    with open_file(yaml_file_path, "w") as yaml_file:
        yaml.dump(yaml_file_content, yaml_file)
