"""
MEENA — Data Pipeline Configuration

Defines configuration parameters for dataset acquisition, conversation reconstruction,
train/val/test splitting, BPE subword tokenization, and PyTorch DataLoaders.
"""

from dataclasses import dataclass, field
from typing import Optional, List
import os
import json


@dataclass
class DataPipelineConfig:
    """
    Configuration for the conversational data and tokenization pipeline.
    Uses relative paths rooted in the ml-service directory for cross-platform portability.
    """
    # Dataset Directories
    base_dir: str = field(
        default_factory=lambda: os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    )
    raw_data_dir: str = "data/raw"
    processed_data_dir: str = "data/processed"
    tokenizer_dir: str = "data/tokenizer"

    # Dataset Sources & Licensing
    dataset_name: str = "oasst1_curated"
    max_conversations: Optional[int] = 10000  # Configurable sample cap for 8GB RAM
    min_turns: int = 2                       # Minimum turns in a conversation
    max_turns_history: int = 3               # Multi-turn context window (last N turns)
    min_token_length: int = 2                # Minimum token count for valid message
    max_seq_len: int = 128                   # Maximum sequence length (tokens)

    # Train / Validation / Test Splitting (Split strictly by conversation ID)
    train_ratio: float = 0.80
    val_ratio: float = 0.10
    test_ratio: float = 0.10
    random_seed: int = 42

    # Tokenizer Specifications (Strictly aligned with EvolvedTransformerConfig)
    vocab_size: int = 8000
    min_frequency: int = 2
    pad_token: str = "<pad>"
    bos_token: str = "<bos>"
    eos_token: str = "<eos>"
    unk_token: str = "<unk>"

    pad_token_id: int = 0
    bos_token_id: int = 1
    eos_token_id: int = 2
    unk_token_id: int = 3

    # DataLoader Specifications (Optimized for 4GB VRAM / 8GB RAM)
    batch_size: int = 4
    num_workers: int = 0  # 0 prevents Windows multiprocessing socket overhead
    pin_memory: bool = False

    def __post_init__(self):
        # Resolve full paths relative to base_dir
        if not os.path.isabs(self.raw_data_dir):
            self.raw_data_dir = os.path.normpath(os.path.join(self.base_dir, self.raw_data_dir))
        if not os.path.isabs(self.processed_data_dir):
            self.processed_data_dir = os.path.normpath(os.path.join(self.base_dir, self.processed_data_dir))
        if not os.path.isabs(self.tokenizer_dir):
            self.tokenizer_dir = os.path.normpath(os.path.join(self.base_dir, self.tokenizer_dir))

        # Validate ratios
        total_ratio = round(self.train_ratio + self.val_ratio + self.test_ratio, 4)
        if total_ratio != 1.0:
            raise ValueError(f"Train, val, and test ratios must sum to 1.0, got {total_ratio}")

    @property
    def special_tokens(self) -> List[str]:
        return [self.pad_token, self.bos_token, self.eos_token, self.unk_token]

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}

    def save_json(self, path: str):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_json(cls, path: str) -> "DataPipelineConfig":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)
