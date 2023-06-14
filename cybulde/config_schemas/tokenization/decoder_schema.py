from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic import validator
from pydantic.dataclasses import dataclass


@dataclass
class DecoderConfig:
    _target_: str = MISSING


@dataclass
class BPEDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.BPEDecoder"
    suffix: str = "</w>"


@dataclass
class ByteLevelDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.ByteLevel"


@dataclass
class CTCDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.CTC"
    pad_token: str = "<pad>"
    word_delimiter_token: str = "|"
    cleanup: bool = True


@dataclass
class MetaspaceDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.Metaspace"
    replacement: str = "_"
    add_prefix_space: bool = True

    @validator("replacement")
    def validate_replacement(cls, replacement: str) -> str:
        if len(replacement) > 1:
            raise ValueError(f"len(replacement) must be 1, got: {len(replacement)}")
        return replacement


@dataclass
class WordPieceDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.Metaspace"
    prefix: str = "##"
    cleanup: bool = True


def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(
        group="tokenizer/decoder",
        name="bpe_decoder_schema",
        node=BPEDecoderConfig,
    )

    cs.store(
        group="tokenizer/decoder",
        name="byte_level_decoder_schema",
        node=ByteLevelDecoderConfig,
    )

    cs.store(
        group="tokenizer/decoder",
        name="ctc_decoder_schema",
        node=CTCDecoderConfig,
    )

    cs.store(
        group="tokenizer/decoder",
        name="metaspace_decoder_schema",
        node=MetaspaceDecoderConfig,
    )

    cs.store(
        group="tokenizer/decoder",
        name="word_piece_decoder_schema",
        node=WordPieceDecoderConfig,
    )
