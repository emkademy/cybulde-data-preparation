from dataclasses import field

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic import validator
from pydantic.dataclasses import dataclass

from cybulde.utils.schema_utils import validate_config_parameter_is_in

SPLIT_DELIMITER_BEHAVIOUR_OPTIONS = {"removed", "isolated", "merged_with_previous", "merged_with_next", "contiguous"}


@dataclass
class PreTokenizerConfig:
    _target_: str = MISSING


@dataclass
class BertPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.BertPreTokenizer"


@dataclass
class ByteLevelPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.ByteLevelPreTokenizer"


@dataclass
class CharDelimiterSplitPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.CharDelimiterSplit"


@dataclass
class DigitsPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.Digits"
    individual_digits: bool = False


@dataclass
class MetaspacePreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.Metaspace"
    replacement: str = "_"
    add_prefix_space: bool = True


@dataclass
class PunctuationPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.Punctuation"
    behavior: str = "isolated"

    @validator("behavior")
    def validate_behavior(cls, behavior: str) -> str:
        validate_config_parameter_is_in(SPLIT_DELIMITER_BEHAVIOUR_OPTIONS, behavior, "behavior")
        return behavior


@dataclass
class SequencePreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.Sequence"
    pretokenizers: list[PreTokenizerConfig] = field(default_factory=lambda: [])
    _pretokenizers_dict: dict[str, PreTokenizerConfig] = field(default_factory=lambda: {})


@dataclass
class SplitPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.Split"
    pattern: str = MISSING
    behavior: str = MISSING
    invert: bool = False

    @validator("behavior")
    def validate_behavior(cls, behavior: str) -> str:
        validate_config_parameter_is_in(SPLIT_DELIMITER_BEHAVIOUR_OPTIONS, behavior, "behavior")
        return behavior


@dataclass
class UnicodeScriptsPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.UnicodeScripts"


@dataclass
class WhitespacePreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.Whitespace"


@dataclass
class WhitespaceSplitPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.WhitespaceSplit"


def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(
        group="tokenizer/pre_tokenizer",
        name="bert_pre_tokenizer_schema",
        node=BertPreTokenizerConfig,
    )

    cs.store(
        group="tokenizer/pre_tokenizer",
        name="byte_level_pre_tokenizer_schema",
        node=ByteLevelPreTokenizerConfig,
    )

    cs.store(
        group="tokenizer/pre_tokenizer",
        name="char_delimiter_split_pre_tokenizer_schema",
        node=CharDelimiterSplitPreTokenizerConfig,
    )

    cs.store(
        group="tokenizer/pre_tokenizer",
        name="digits_pre_tokenizer_schema",
        node=DigitsPreTokenizerConfig,
    )

    cs.store(
        group="tokenizer/pre_tokenizer",
        name="metaspace_pre_tokenizer_schema",
        node=MetaspacePreTokenizerConfig,
    )

    cs.store(
        group="tokenizer/pre_tokenizer",
        name="punctuation_pre_tokenizer_schema",
        node=PunctuationPreTokenizerConfig,
    )

    cs.store(
        group="tokenizer/pre_tokenizer",
        name="sequence_pre_tokenizer_schema",
        node=SequencePreTokenizerConfig,
    )

    cs.store(
        group="tokenizer/pre_tokenizer",
        name="split_pre_tokenizer_schema",
        node=SplitPreTokenizerConfig,
    )

    cs.store(
        group="tokenizer/pre_tokenizer",
        name="unicode_scripts_pre_tokenizer_schema",
        node=UnicodeScriptsPreTokenizerConfig,
    )

    cs.store(
        group="tokenizer/pre_tokenizer",
        name="whitespace_pre_tokenizer_schema",
        node=WhitespacePreTokenizerConfig,
    )

    cs.store(
        group="tokenizer/pre_tokenizer",
        name="whitespace_split_pre_tokenizer_schema",
        node=WhitespaceSplitPreTokenizerConfig,
    )
