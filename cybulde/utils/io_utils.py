from typing import Any

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
