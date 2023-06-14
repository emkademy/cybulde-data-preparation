from dataclasses import field

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass


@dataclass
class NormalizerConfig:
    _target_: str = MISSING


@dataclass
class BertNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.BertNormalizer"
    clean_text: bool = True
    handle_chinese_chars: bool = True
    strip_accents: bool = True
    lowercase: bool = True


@dataclass
class LowercaseNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.Lowercase"


@dataclass
class NFCNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.NFC"


@dataclass
class NFDNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.NFD"


@dataclass
class NFKCNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.NFKC"


@dataclass
class NFKDNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.NFKD"


@dataclass
class NmtNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.Nmt"


@dataclass
class ReplaceNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.Nmt"
    pattern: str = MISSING
    content: str = MISSING


@dataclass
class SequenceNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.Sequence"
    normalizers: list[NormalizerConfig] = field(default_factory=lambda: [])
    _normalizers_dict: dict[str, NormalizerConfig] = field(default_factory=lambda: {})


@dataclass
class StripNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.Strip"
    left: bool = True
    right: bool = True


@dataclass
class StripAccentsNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.StripAccents"


def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(
        group="tokenizer/normalizer",
        name="bert_normalizer_schema",
        node=BertNormalizerConfig,
    )

    cs.store(
        group="tokenizer/normalizer",
        name="liwer_case_normalizer_schema",
        node=LowercaseNormalizerConfig,
    )

    cs.store(
        group="tokenizer/normalizer",
        name="lower_case_normalizer_schema",
        node=LowercaseNormalizerConfig,
    )

    cs.store(
        group="tokenizer/normalizer",
        name="nfc_normalizer_schema",
        node=NFCNormalizerConfig,
    )

    cs.store(
        group="tokenizer/normalizer",
        name="nfd_normalizer_schema",
        node=NFDNormalizerConfig,
    )

    cs.store(
        group="tokenizer/normalizer",
        name="nfkc_normalizer_schema",
        node=NFKCNormalizerConfig,
    )

    cs.store(
        group="tokenizer/normalizer",
        name="nfkd_normalizer_schema",
        node=NFKDNormalizerConfig,
    )

    cs.store(
        group="tokenizer/normalizer",
        name="nmt_normalizer_schema",
        node=NmtNormalizerConfig,
    )

    cs.store(
        group="tokenizer/normalizer",
        name="replace_normalizer_schema",
        node=ReplaceNormalizerConfig,
    )

    cs.store(
        group="tokenizer/normalizer",
        name="sequence_normalizer_schema",
        node=SequenceNormalizerConfig,
    )

    cs.store(
        group="tokenizer/normalizer",
        name="strip_normalizer_schema",
        node=StripNormalizerConfig,
    )

    cs.store(
        group="tokenizer/normalizer",
        name="strip_accent_normalizer_schema",
        node=StripAccentsNormalizerConfig,
    )
