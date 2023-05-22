from __future__ import annotations

import re
import string

from abc import ABC, abstractmethod

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from cybulde.utils.utils import SpellCorrectionModel


class DatasetCleaner(ABC):
    def __call__(self, text: str | list[str]) -> str | list[str]:
        if isinstance(text, str):
            return self.clean_text(text)
        return self.clean_words(text)

    @abstractmethod
    def clean_text(self, text: str) -> str:
        """
        Cleans the given string
        """

    @abstractmethod
    def clean_words(self, words: list[str]) -> list[str]:
        """
        Cleans each word in a list of words
        """


class StopWordsDatasetCleaner(DatasetCleaner):
    def __init__(self) -> None:
        super().__init__()
        self.stopwords = set(stopwords.words("english"))

    def clean_text(self, text: str) -> str:
        cleaned_text = [word for word in word_tokenize(text) if word not in self.stopwords]
        return " ".join(cleaned_text)

    def clean_words(self, words: list[str]) -> list[str]:
        return [word for word in words if word not in self.stopwords]


class ToLowerCaseDatasetCleaner(DatasetCleaner):
    def clean_text(self, text: str) -> str:
        return text.lower()

    def clean_words(self, words: list[str]) -> list[str]:
        return [word.lower() for word in words]


class URLDatasetCleaner(DatasetCleaner):
    def clean_text(self, text: str) -> str:
        return re.sub(r"http\S+", "", text, flags=re.MULTILINE)

    def clean_words(self, words: list[str]) -> list[str]:
        return [self.clean_text(word) for word in words]


class PunctuationDatasetCleaner(DatasetCleaner):
    def __init__(self, punctuation: str = string.punctuation) -> None:
        super().__init__()
        self.table = str.maketrans("", "", punctuation)

    def clean_text(self, text: str) -> str:
        return " ".join(self.clean_words(text.split()))

    def clean_words(self, words: list[str]) -> list[str]:
        return [word.translate(self.table) for word in words if word.translate(self.table)]


class NonLettersDatasetCleaner(DatasetCleaner):
    def clean_text(self, text: str) -> str:
        return " ".join(self.clean_words(text.split()))

    def clean_words(self, words: list[str]) -> list[str]:
        return [word for word in words if word.isalpha()]


class NewLineCharacterDatasetCleaner(DatasetCleaner):
    def clean_text(self, text: str) -> str:
        return text.replace("\n", "")

    def clean_words(self, words: list[str]) -> list[str]:
        return [self.clean_text(word) for word in words]


class NonASCIIDatasetCleaner(DatasetCleaner):
    def clean_text(self, text: str) -> str:
        return " ".join(self.clean_words(text.split()))

    def clean_words(self, words: list[str]) -> list[str]:
        return [word for word in words if word.isascii()]


class ReferanceToAccountDatasetCleaner(DatasetCleaner):
    def clean_text(self, text: str) -> str:
        return re.sub(r"@\w+", "", text)

    def clean_words(self, words: list[str]) -> list[str]:
        text = " ".join(words)
        return self.clean_text(text).split()


class ReTweetDatasetCleaner(DatasetCleaner):
    def clean_text(self, text: str) -> str:
        return re.sub(r"\bRT\b", "", text, flags=re.IGNORECASE)

    def clean_words(self, words: list[str]) -> list[str]:
        text = " ".join(words)
        return self.clean_text(text).split()


class SpellCorrectionDatasetCleaner(DatasetCleaner):
    def __init__(self, spell_correction_model: SpellCorrectionModel) -> None:
        super().__init__()
        self.spell_correction_model = spell_correction_model

    def clean_text(self, text: str) -> str:
        return self.spell_correction_model(text)

    def clean_words(self, words: list[str]) -> list[str]:
        text = " ".join(words)
        return self.clean_text(text).split()


class CharacterLimiterDatasetCleaner(DatasetCleaner):
    def __init__(self, character_limit: int = 300) -> None:
        super().__init__()
        self.character_limit = character_limit

    def clean_text(self, text: str) -> str:
        return text[: self.character_limit]

    def clean_words(self, words: list[str]) -> list[str]:
        text = " ".join(words)
        return self.clean_text(text).split()


class DatasetCleanerManager:
    def __init__(self, dataset_cleaners: dict[str, DatasetCleaner]) -> None:
        self.dataset_cleaners = dataset_cleaners

    def __call__(self, text: str | list[str]) -> str | list[str]:
        for dataset_cleaner in self.dataset_cleaners.values():
            text = dataset_cleaner(text)
        return text
