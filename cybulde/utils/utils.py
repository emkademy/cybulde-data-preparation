import logging
import socket
import subprocess

import pkg_resources
import symspellpy

from symspellpy import SymSpell


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"[{socket.gethostname()}] {name}")


def run_shell_command(cmd: str) -> str:
    return subprocess.run(cmd, text=True, shell=True, check=True, capture_output=True).stdout


class SpellCorrectionModel:
    def __init__(
        self,
        max_dictionary_edit_distance: int = 2,
        prefix_length: int = 7,
        count_threshold: int = 1,
    ) -> None:
        self.max_dictionary_edit_distance = max_dictionary_edit_distance
        self.model = self._initialize_model(prefix_length, count_threshold)

    def _initialize_model(self, prefix_length: int, count_threshold: int) -> symspellpy.symspellpy.SymSpell:
        model = SymSpell(self.max_dictionary_edit_distance, prefix_length, count_threshold)

        dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
        bigram_dictionary_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_bigramdictionary_en_243_342.txt"
        )

        model.load_dictionary(dictionary_path, 0, 1)
        model.load_bigram_dictionary(bigram_dictionary_path, 0, 2)
        return model

    def __call__(self, text: str) -> str:
        suggestion: str = self.model.lookup_compound(text, max_edit_distance=self.max_dictionary_edit_distance)[0].term
        return suggestion
