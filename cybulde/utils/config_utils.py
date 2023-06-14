import argparse
import importlib
import logging
import logging.config
import os
import pickle

from dataclasses import asdict
from functools import partial
from io import BytesIO, StringIO
from typing import Any, Optional

import hydra
import yaml

from hydra import compose, initialize
from hydra.types import TaskFunction
from omegaconf import DictConfig, OmegaConf

from cybulde.config_schemas import data_processing_config_schema, tokenizer_training_config_schema
from cybulde.utils.io_utils import open_file


def get_config(config_path: str, config_name: str) -> TaskFunction:
    setup_config()
    setup_logger()

    def main_decorator(task_function: TaskFunction) -> Any:
        @hydra.main(config_path=config_path, config_name=config_name, version_base=None)
        def decorated_main(dict_config: Optional[DictConfig] = None) -> Any:
            config = OmegaConf.to_object(dict_config)
            return task_function(config)

        return decorated_main

    return main_decorator


def get_pickle_config(config_path: str, config_name: str) -> TaskFunction:
    setup_config()
    setup_logger()

    def main_decorator(task_function: TaskFunction) -> Any:
        def decorated_main() -> Any:
            config = load_pickle_config(config_path, config_name)
            return task_function(config)

        return decorated_main

    return main_decorator


def load_pickle_config(config_path: str, config_name: str) -> Any:
    with open_file(os.path.join(config_path, f"{config_name}.pickle"), "rb") as f:
        config = pickle.load(f)
    return config


def setup_config() -> None:
    data_processing_config_schema.setup_config()
    tokenizer_training_config_schema.setup_config()


def setup_logger() -> None:
    with open("./cybulde/configs/hydra/job_logging/custom.yaml", "r") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)


def config_args_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--config-path", type=str, default="../configs/", help="Directory of the config files")
    parser.add_argument("--config-name", type=str, required=True, help="Name of the config file")
    parser.add_argument("--overrides", nargs="*", help="Hydra config overrides", default=[])

    return parser.parse_args()


def compose_config(config_path: str, config_name: str, overrides: Optional[list[str]] = None) -> Any:
    setup_config()
    setup_logger()

    if overrides is None:
        overrides = []

    with initialize(version_base=None, config_path=config_path, job_name="config-compose"):
        dict_config = compose(config_name=config_name, overrides=overrides)
        config = OmegaConf.to_object(dict_config)
    return config


def save_config_as_yaml(config: Any, save_path: str) -> None:
    text_io = StringIO()
    OmegaConf.save(config, text_io, resolve=True)
    with open_file(save_path, "w") as f:
        f.write(text_io.getvalue())


def save_config_as_pickle(config: Any, save_path: str) -> None:
    bytes_io = BytesIO()
    pickle.dump(config, bytes_io)
    with open_file(save_path, "wb") as f:
        f.write(bytes_io.getvalue())


def custom_instantiate(config: Any) -> Any:
    config_as_dict = asdict(config)
    if "_target_" not in config_as_dict:
        raise ValueError("Config does not have _target_ key")

    _target_ = config_as_dict["_target_"]
    _partial_ = config_as_dict.get("_partial_", False)

    config_as_dict.pop("_target_", None)
    config_as_dict.pop("_partial_", None)

    splitted_target = _target_.split(".")
    module_name, class_name = ".".join(splitted_target[:-1]), splitted_target[-1]

    module = importlib.import_module(module_name)
    _class = getattr(module, class_name)
    if _partial_:
        return partial(_class, **config_as_dict)
    return _class(**config_as_dict)
