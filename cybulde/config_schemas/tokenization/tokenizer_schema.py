from typing import Optional

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass

import cybulde.config_schemas.tokenization.decoder_schema as decoder_schemas
import cybulde.config_schemas.tokenization.model_schema as model_schemas
import cybulde.config_schemas.tokenization.normalizer_schema as normalizer_schemas
import cybulde.config_schemas.tokenization.post_processor_schema as post_processor_schemas
import cybulde.config_schemas.tokenization.pre_tokenizer_schema as pre_tokenizer_schemas
import cybulde.config_schemas.tokenization.trainer_schema as trainer_schemas


@dataclass
class TokenizerConfig:
    _target_: str = MISSING


@dataclass
class HuggigFaceTokenizerConfig(TokenizerConfig):
    _target_: str = "cybulde.tokenization.tokenizers.HuggingFaceTokenizer"
    pre_tokenizer: pre_tokenizer_schemas.PreTokenizerConfig = MISSING
    model: model_schemas.ModelConfig = MISSING
    trainer: trainer_schemas.TrainerConfig = MISSING
    normalizer: Optional[normalizer_schemas.NormalizerConfig] = None
    decoder: Optional[decoder_schemas.DecoderConfig] = None
    post_processor: Optional[post_processor_schemas.PostProcessorConfig] = None

    unk_token: Optional[str] = "[UNK]"
    cls_token: Optional[str] = "[CLS]"
    sep_token: Optional[str] = "[SEP]"
    pad_token: Optional[str] = "[PAD]"
    mask_token: Optional[str] = "[MASK]"


def setup_config() -> None:
    normalizer_schemas.setup_config()
    post_processor_schemas.setup_config()
    pre_tokenizer_schemas.setup_config()
    model_schemas.setup_config()
    trainer_schemas.setup_config()
    decoder_schemas.setup_config()

    cs = ConfigStore.instance()

    cs.store(
        group="tokenizer",
        name="hugging_face_tokenizer_schema",
        node=HuggigFaceTokenizerConfig,
    )
