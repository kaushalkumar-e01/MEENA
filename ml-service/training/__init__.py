"""
MEENA — Neural Training Pipeline Package

Implements end-to-end PyTorch training, validation, teacher forcing,
hardware optimization, and checkpoint management for the MEENA Evolved Transformer.
"""

from .config import TrainingConfig
from .trainer import MeenaTrainer

__all__ = ["TrainingConfig", "MeenaTrainer"]

