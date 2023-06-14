from typing import Any, Optional

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, SI
from pydantic.dataclasses import dataclass


@dataclass
class ModelConfig:
    _target_: str = MISSING


@dataclass
class BPEModelConfig(ModelConfig):
    _target_: str = "tokenizers.models.BPE"
    vocab: Optional[dict[str, int]] = None
    merges: Optional[list[Any]] = None
    cache_capacity: int = 10_000
    dropout: Optional[float] = None
    unk_token: Optional[str] = SI("${tokenizer.unk_token}")
    fuse_unk: bool = False


@dataclass
class UnigramModelConfig(ModelConfig):
    _target_: str = "tokenizers.models.Unigram"
    vocab: Optional[dict[str, float]] = None


@dataclass
class WordLevelModelConfig(ModelConfig):
    _target_: str = "tokenizers.models.WordLevel"
    vocab: Optional[dict[str, int]] = None
    unk_token: Optional[str] = SI("${tokenizer.unk_token}")


@dataclass
class WordPieceModelConfig(ModelConfig):
    _target_: str = "tokenizers.models.WordPiece"
    vocab: Optional[dict[str, int]] = None
    unk_token: Optional[str] = SI("${tokenizers.unk_token}")
    max_input_chars_per_word: Optional[int] = None


def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(
        group="tokenizer/model",
        name="bpe_model_schema",
        node=BPEModelConfig,
    )

    cs.store(
        group="tokenizer/model",
        name="unigram_model_schema",
        node=UnigramModelConfig,
    )

    cs.store(
        group="tokenizer/model",
        name="word_level_model_schema",
        node=WordLevelModelConfig,
    )

    cs.store(
        group="tokenizer/model",
        name="word_piece_model_schema",
        node=WordPieceModelConfig,
    )
