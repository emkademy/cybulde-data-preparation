from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass


@dataclass
class PostProcessorConfig:
    _target_: str = MISSING


@dataclass
class BertPostProcessorConfig(PostProcessorConfig):
    _target_: str = "tokenizers.processors.BertProcessing"
    sep: tuple[str, int] = MISSING
    cls: tuple[str, int] = MISSING


@dataclass
class ByteLevelPostProcessorConfig(PostProcessorConfig):
    _target_: str = "tokenizers.processors.ByteLevel"
    trim_offset: bool = True


@dataclass
class RobertaPostProcessorConfig(PostProcessorConfig):
    _target_: str = "tokenizers.processors.RobertaProcessing"
    sep: tuple[str, int] = MISSING
    cls: tuple[str, int] = MISSING
    trim_offset: bool = True
    add_prefix_space: bool = True


def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(
        group="tokenizer/post_processor",
        name="bert_post_processing_schema",
        node=BertPostProcessorConfig,
    )

    cs.store(
        group="tokenizer/post_processor",
        name="byte_level_post_processing_schema",
        node=ByteLevelPostProcessorConfig,
    )

    cs.store(
        group="tokenizer/post_processor",
        name="roberta_post_processing_schema",
        node=RobertaPostProcessorConfig,
    )
