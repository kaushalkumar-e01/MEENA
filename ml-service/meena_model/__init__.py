"""
MEENA Neural Architecture Package

Exposes the Evolved Transformer model, configuration, and components.
"""

from .config import EvolvedTransformerConfig
from .model import MeenaEvolvedTransformer
from .encoder import EvolvedTransformerEncoder, EvolvedTransformerEncoderLayer
from .decoder import EvolvedTransformerDecoder, EvolvedTransformerDecoderLayer
from .modules import (
    PositionalEncoding,
    GatedLinearUnit,
    DepthwiseSeparableConv1d,
    CausalDepthwiseSeparableConv1d,
    MultiHeadAttention,
    FeedForward
)

__all__ = [
    "EvolvedTransformerConfig",
    "MeenaEvolvedTransformer",
    "EvolvedTransformerEncoder",
    "EvolvedTransformerEncoderLayer",
    "EvolvedTransformerDecoder",
    "EvolvedTransformerDecoderLayer",
    "PositionalEncoding",
    "GatedLinearUnit",
    "DepthwiseSeparableConv1d",
    "CausalDepthwiseSeparableConv1d",
    "MultiHeadAttention",
    "FeedForward"
]
