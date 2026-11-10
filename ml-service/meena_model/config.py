"""
MEENA — Evolved Transformer Architecture Configuration

Implements the official architectural specifications inspired by Adiwardana et al. (2020)
and the Evolved Transformer discovered by So et al. (ICML 2019):
- Exactly 1 Evolved Transformer Encoder block
- Exactly 13 Evolved Transformer Decoder blocks
"""

from dataclasses import dataclass, field
from typing import Optional, Literal
import json
import os


@dataclass
class EvolvedTransformerConfig:
    """
    Configuration dataclass for the MEENA Evolved Transformer model.
    Default parameters are optimized for a compact 4GB VRAM footprint (RTX 3050).
    """
    # Architecture layer counts (STRICT SPECIFICATION)
    num_encoder_layers: int = 1
    num_decoder_layers: int = 13

    # Dimensionality & Capacity (compact defaults for 4GB VRAM)
    d_model: int = 128
    n_heads: int = 4
    d_ff: int = 512
    max_seq_len: int = 128
    vocab_size: int = 8000

    # Evolved Transformer specific hyper-parameters
    kernel_size_enc: int = 9      # Wide depthwise separable convolution kernel in encoder
    kernel_size_dec: int = 11     # Wide causal depthwise separable convolution kernel in decoder
    glu_activation: Literal["glu", "swiglu"] = "glu"
    activation: Literal["swish", "relu", "gelu"] = "swish"
    dropout: float = 0.1
    layer_norm_eps: float = 1e-5

    # Hardware & Memory Optimizations
    use_gradient_checkpointing: bool = True
    mixed_precision: Literal["fp16", "bf16", "fp32"] = "fp16"
    tie_word_embeddings: bool = True

    # Special token indices
    pad_token_id: int = 0
    bos_token_id: int = 1
    eos_token_id: int = 2
    unk_token_id: int = 3

    def __post_init__(self):
        # Strict validation
        if self.num_encoder_layers != 1:
            raise ValueError(
                f"MEENA architecture requires exactly 1 encoder block, got {self.num_encoder_layers}"
            )
        if self.num_decoder_layers != 13:
            raise ValueError(
                f"MEENA architecture requires exactly 13 decoder blocks, got {self.num_decoder_layers}"
            )
        if self.d_model % self.n_heads != 0:
            raise ValueError(
                f"d_model ({self.d_model}) must be divisible by n_heads ({self.n_heads})"
            )
        if self.kernel_size_enc % 2 == 0:
            raise ValueError("kernel_size_enc must be odd for symmetric padding")
        if self.kernel_size_dec % 2 == 0:
            raise ValueError("kernel_size_dec must be odd for causal convolution")

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, data: dict) -> "EvolvedTransformerConfig":
        return cls(**data)

    def save_json(self, path: str):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_json(cls, path: str) -> "EvolvedTransformerConfig":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
