"""
MEENA — Neural Model Training Configuration

Defines hyper-parameters, hardware optimization switches, checkpoint policies,
and runtime settings for training the 1-Encoder + 13-Decoder Evolved Transformer.
"""

from dataclasses import dataclass, field
from typing import Optional, Literal
import os
import json


@dataclass
class TrainingConfig:
    """
    Configuration dataclass for the MEENA Evolved Transformer training pipeline.
    Tailored for 4GB VRAM GPU (RTX 3050) and 8GB system RAM constraints.
    """
    # Directory paths (relative to ml-service root or absolute)
    base_dir: str = field(
        default_factory=lambda: os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    )
    processed_data_dir: str = "data/processed"
    tokenizer_dir: str = "data/tokenizer"
    checkpoint_dir: str = "checkpoints"
    output_dir: str = "outputs"

    # Training Hyperparameters
    batch_size: int = 4                    # Micro-batch size per forward pass
    gradient_accumulation_steps: int = 4  # Effective batch size = 4 * 4 = 16
    learning_rate: float = 5e-4
    weight_decay: float = 0.01
    adam_beta1: float = 0.9
    adam_beta2: float = 0.98
    adam_eps: float = 1e-8
    max_grad_norm: float = 1.0             # Gradient clipping threshold
    num_epochs: int = 5
    warmup_steps: int = 50
    lr_scheduler_type: Literal["cosine", "linear", "constant"] = "cosine"
    label_smoothing: float = 0.1
    min_lr_ratio: float = 0.1              # Final LR is 10% of peak LR in cosine

    # Hardware & Performance Optimizations (RTX 3050 / 8GB RAM)
    device: Literal["auto", "cuda", "cpu"] = "auto"
    mixed_precision: Literal["fp16", "bf16", "fp32"] = "fp16"
    use_gradient_checkpointing: bool = True
    num_workers: int = 0                   # 0 avoids Windows multiprocessing overhead
    pin_memory: bool = False

    # Checkpoint & Validation Management
    save_every_n_epochs: int = 1
    eval_every_n_epochs: int = 1
    keep_last_n_checkpoints: int = 3
    resume_from_checkpoint: Optional[str] = None
    random_seed: int = 42
    max_train_batches: Optional[int] = None
    max_val_batches: Optional[int] = None

    # Logging & Monitoring
    log_interval: int = 10                 # Log training loss every N batches

    def __post_init__(self):
        # Resolve full paths relative to base_dir
        if not os.path.isabs(self.processed_data_dir):
            self.processed_data_dir = os.path.normpath(os.path.join(self.base_dir, self.processed_data_dir))
        if not os.path.isabs(self.tokenizer_dir):
            self.tokenizer_dir = os.path.normpath(os.path.join(self.base_dir, self.tokenizer_dir))
        if not os.path.isabs(self.checkpoint_dir):
            self.checkpoint_dir = os.path.normpath(os.path.join(self.base_dir, self.checkpoint_dir))
        if not os.path.isabs(self.output_dir):
            self.output_dir = os.path.normpath(os.path.join(self.base_dir, self.output_dir))

        # Ensure directories exist
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        if self.batch_size <= 0:
            raise ValueError(f"batch_size must be positive, got {self.batch_size}")
        if self.gradient_accumulation_steps <= 0:
            raise ValueError(f"gradient_accumulation_steps must be positive, got {self.gradient_accumulation_steps}")
        if self.learning_rate <= 0:
            raise ValueError(f"learning_rate must be positive, got {self.learning_rate}")

    @property
    def effective_batch_size(self) -> int:
        return self.batch_size * self.gradient_accumulation_steps

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, data: dict) -> "TrainingConfig":
        return cls(**data)

    def save_json(self, path: str):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_json(cls, path: str) -> "TrainingConfig":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

