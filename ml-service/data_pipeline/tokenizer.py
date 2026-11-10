"""
MEENA — Subword Byte-Pair Encoding (BPE) Tokenizer

Implements a reproducible Byte-Pair Encoding subword tokenizer using the HuggingFace
tokenizers backend with strict special token ID guarantees:
- Index 0: <pad> (Padding token)
- Index 1: <bos> (Beginning of sequence)
- Index 2: <eos> (End of sequence)
- Index 3: <unk> (Unknown token)
Matches EvolvedTransformerConfig exactly.
"""

import os
import json
from typing import List, Union, Iterator, Optional
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import ByteLevel
from tokenizers.decoders import ByteLevel as ByteLevelDecoder

from .config import DataPipelineConfig


class MeenaTokenizer:
    """
    Wrapper around HuggingFace ByteLevel BPE Tokenizer ensuring strict special token
    indexing and reproducible serialization for the MEENA Evolved Transformer.
    """
    def __init__(self, tokenizer: Optional[Tokenizer] = None, config: Optional[DataPipelineConfig] = None):
        self.config = config or DataPipelineConfig()
        self.tokenizer = tokenizer

        self.pad_token = self.config.pad_token
        self.bos_token = self.config.bos_token
        self.eos_token = self.config.eos_token
        self.unk_token = self.config.unk_token

        self.pad_token_id = self.config.pad_token_id
        self.bos_token_id = self.config.bos_token_id
        self.eos_token_id = self.config.eos_token_id
        self.unk_token_id = self.config.unk_token_id

        if self.tokenizer is not None:
            self._verify_special_tokens()

    def _verify_special_tokens(self):
        """Validates that special tokens map to their designated integer IDs."""
        id_pad = self.tokenizer.token_to_id(self.pad_token)
        id_bos = self.tokenizer.token_to_id(self.bos_token)
        id_eos = self.tokenizer.token_to_id(self.eos_token)
        id_unk = self.tokenizer.token_to_id(self.unk_token)

        assert id_pad == self.pad_token_id, f"PAD token ID mismatch: expected {self.pad_token_id}, got {id_pad}"
        assert id_bos == self.bos_token_id, f"BOS token ID mismatch: expected {self.bos_token_id}, got {id_bos}"
        assert id_eos == self.eos_token_id, f"EOS token ID mismatch: expected {self.eos_token_id}, got {id_eos}"
        assert id_unk == self.unk_token_id, f"UNK token ID mismatch: expected {self.unk_token_id}, got {id_unk}"

    @classmethod
    def train_from_iterator(
        cls,
        texts: Iterator[str],
        config: Optional[DataPipelineConfig] = None
    ) -> "MeenaTokenizer":
        """
        Trains a new ByteLevel BPE tokenizer on a stream/iterator of text strings.
        Strictly trains ONLY on the training split.
        """
        cfg = config or DataPipelineConfig()

        # 1. Initialize empty BPE model with <unk> token
        raw_tokenizer = Tokenizer(BPE(unk_token=cfg.unk_token))
        raw_tokenizer.pre_tokenizer = ByteLevel(add_prefix_space=False)
        raw_tokenizer.decoder = ByteLevelDecoder()

        # 2. Configure BPE Trainer
        trainer = BpeTrainer(
            vocab_size=cfg.vocab_size,
            min_frequency=cfg.min_frequency,
            special_tokens=cfg.special_tokens,
            show_progress=False
        )

        # 3. Train on iterator
        raw_tokenizer.train_from_iterator(texts, trainer=trainer)

        return cls(raw_tokenizer, cfg)

    @classmethod
    def train_from_files(
        cls,
        files: List[str],
        config: Optional[DataPipelineConfig] = None
    ) -> "MeenaTokenizer":
        """
        Trains the tokenizer directly from one or more text files.
        """
        cfg = config or DataPipelineConfig()

        raw_tokenizer = Tokenizer(BPE(unk_token=cfg.unk_token))
        raw_tokenizer.pre_tokenizer = ByteLevel(add_prefix_space=False)
        raw_tokenizer.decoder = ByteLevelDecoder()

        trainer = BpeTrainer(
            vocab_size=cfg.vocab_size,
            min_frequency=cfg.min_frequency,
            special_tokens=cfg.special_tokens,
            show_progress=False
        )

        raw_tokenizer.train(files, trainer=trainer)
        return cls(raw_tokenizer, cfg)

    def encode(self, text: str, add_special_tokens: bool = False) -> List[int]:
        """
        Encodes a string into a list of subword token IDs.
        If add_special_tokens is True, wraps with <bos> and <eos>.
        """
        if self.tokenizer is None:
            raise RuntimeError("Tokenizer is not loaded or trained yet.")

        encoded = self.tokenizer.encode(text)
        token_ids = encoded.ids

        if add_special_tokens:
            return [self.bos_token_id] + token_ids + [self.eos_token_id]
        return token_ids

    def decode(self, ids: List[int], skip_special_tokens: bool = True) -> str:
        """
        Decodes a list of integer token IDs back into human-readable text.
        """
        if self.tokenizer is None:
            raise RuntimeError("Tokenizer is not loaded or trained yet.")

        if skip_special_tokens:
            filtered_ids = [
                i for i in ids
                if i not in (self.pad_token_id, self.bos_token_id, self.eos_token_id)
            ]
            return self.tokenizer.decode(filtered_ids)
        return self.tokenizer.decode(ids)

    def save(self, directory_path: str):
        """
        Saves the tokenizer definition and metadata JSON.
        """
        os.makedirs(directory_path, exist_ok=True)
        tokenizer_file = os.path.join(directory_path, "tokenizer.json")
        self.tokenizer.save(tokenizer_file)

        config_file = os.path.join(directory_path, "tokenizer_config.json")
        meta = {
            "pad_token": self.pad_token,
            "bos_token": self.bos_token,
            "eos_token": self.eos_token,
            "unk_token": self.unk_token,
            "pad_token_id": self.pad_token_id,
            "bos_token_id": self.bos_token_id,
            "eos_token_id": self.eos_token_id,
            "unk_token_id": self.unk_token_id,
            "vocab_size": self.get_vocab_size()
        }
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

    @classmethod
    def load(cls, directory_path: str, config: Optional[DataPipelineConfig] = None) -> "MeenaTokenizer":
        """
        Loads a pre-trained tokenizer from disk.
        """
        tokenizer_file = os.path.join(directory_path, "tokenizer.json")
        if not os.path.exists(tokenizer_file):
            raise FileNotFoundError(f"Tokenizer file not found at {tokenizer_file}")

        raw_tokenizer = Tokenizer.from_file(tokenizer_file)
        return cls(raw_tokenizer, config)

    def get_vocab_size(self) -> int:
        if self.tokenizer is None:
            return 0
        return self.tokenizer.get_vocab_size()

    def __len__(self) -> int:
        return self.get_vocab_size()
