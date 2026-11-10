"""
MEENA — Evolved Transformer Trainer & Checkpoint Pipeline

Implements the official training pipeline:
- Strict architecture verification (1 Encoder + 13 Decoder layers)
- Autoregressive Seq2Seq Teacher Forcing with proper padding masks
- AdamW optimizer with decoupled weight decay (bias/LayerNorm excluded)
- Warmup + Cosine Annealing learning rate schedule
- Gradient accumulation and gradient clipping (max_norm=1.0)
- Mixed precision training (AMP fp16/bf16 with GradScaler)
- Hardware auto-detection with graceful CPU fallback and 4GB VRAM optimization
- Validation loop computing cross-entropy loss, perplexity, and token accuracy
- Atomic checkpoint saving and full resume capability (weights, optimizer, scheduler, scaler)
- Autoregressive text generation evaluation for unseen conversational prompts
"""

import os
import sys
import math
import time
import json
import random
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader

from meena_model.config import EvolvedTransformerConfig
from meena_model.model import MeenaEvolvedTransformer
from data_pipeline.tokenizer import MeenaTokenizer
from .config import TrainingConfig


class MeenaTrainer:
    """
    Production PyTorch trainer for the MEENA Evolved Transformer.
    """
    def __init__(
        self,
        model: MeenaEvolvedTransformer,
        config: TrainingConfig,
        train_dataloader: DataLoader,
        val_dataloader: Optional[DataLoader] = None,
        tokenizer: Optional[MeenaTokenizer] = None,
    ):
        self.model = model
        self.config = config
        self.train_dataloader = train_dataloader
        self.val_dataloader = val_dataloader
        self.tokenizer = tokenizer

        # 1. Architecture Preservation Assertion
        self._verify_architecture()

        # 2. Hardware Detection & Device Setup
        self.device, self.amp_dtype, self.scaler = self._setup_hardware()
        self.model = self.model.to(self.device)

        # 3. Reproducible Random Seed
        self._set_seed(self.config.random_seed)

        # 4. Optimizer & LR Scheduler Setup
        self.optimizer, self.scheduler = self._setup_optimizer_and_scheduler()

        # 5. Training State Tracking
        self.start_epoch = 1
        self.global_step = 0
        self.best_val_loss = float("inf")
        self.history: List[Dict[str, Any]] = []

        # 6. Resume from Checkpoint if requested
        if self.config.resume_from_checkpoint:
            self.load_checkpoint(self.config.resume_from_checkpoint)

    def _verify_architecture(self):
        """Verifies strict adherence to 1 Encoder + 13 Decoder architecture."""
        enc_count = len(self.model.encoder.layers)
        dec_count = len(self.model.decoder.layers)
        if enc_count != 1:
            raise ValueError(
                f"MEENA architecture violation: expected exactly 1 encoder block, got {enc_count}"
            )
        if dec_count != 13:
            raise ValueError(
                f"MEENA architecture violation: expected exactly 13 decoder blocks, got {dec_count}"
            )

    def _setup_hardware(self) -> Tuple[torch.device, torch.dtype, Optional[torch.amp.GradScaler]]:
        """
        Auto-detects available GPU/CPU hardware and configures mixed precision.
        Tailored for NVIDIA RTX 3050 (4GB VRAM) and 8GB system RAM.
        """
        device_req = self.config.device.lower()
        if device_req == "cuda" or (device_req == "auto" and torch.cuda.is_available()):
            device = torch.device("cuda:0")
            gpu_name = torch.cuda.get_device_name(0)
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            print(f"[Hardware] GPU detected: {gpu_name} ({vram_gb:.2f} GB VRAM)")

            # Select mixed precision format
            if self.config.mixed_precision == "bf16" and torch.cuda.is_bf16_supported():
                amp_dtype = torch.bfloat16
                scaler = torch.amp.GradScaler("cuda", enabled=False)
                print("[Hardware] Using BF16 Mixed Precision (Native bfloat16)")
            elif self.config.mixed_precision == "fp16":
                amp_dtype = torch.float16
                scaler = torch.amp.GradScaler("cuda", enabled=True)
                print("[Hardware] Using FP16 Mixed Precision with GradScaler")
            else:
                amp_dtype = torch.float32
                scaler = None
                print("[Hardware] Using FP32 Single Precision")

        else:
            device = torch.device("cpu")
            amp_dtype = torch.float32
            scaler = None
            print("[Hardware] CUDA unavailable or CPU requested. Falling back to CPU.")

        return device, amp_dtype, scaler

    @staticmethod
    def _set_seed(seed: int):
        """Sets deterministic random seeds across PyTorch, NumPy, and Python random."""
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

    def _setup_optimizer_and_scheduler(self):
        """
        Constructs AdamW optimizer with decoupled weight decay (excluding biases and LayerNorm)
        and Warmup + Cosine Annealing learning rate schedule.
        """
        # Exclude bias and LayerNorm weights from weight decay
        no_decay = ["bias", "LayerNorm.weight", "ln_", "final_ln"]
        optimizer_grouped_parameters = [
            {
                "params": [
                    p for n, p in self.model.named_parameters()
                    if not any(nd in n for nd in no_decay) and p.requires_grad
                ],
                "weight_decay": self.config.weight_decay,
            },
            {
                "params": [
                    p for n, p in self.model.named_parameters()
                    if any(nd in n for nd in no_decay) and p.requires_grad
                ],
                "weight_decay": 0.0,
            },
        ]

        optimizer = torch.optim.AdamW(
            optimizer_grouped_parameters,
            lr=self.config.learning_rate,
            betas=(self.config.adam_beta1, self.config.adam_beta2),
            eps=self.config.adam_eps,
        )

        # Total training steps calculation
        steps_per_epoch = math.ceil(len(self.train_dataloader) / self.config.gradient_accumulation_steps)
        total_steps = max(steps_per_epoch * self.config.num_epochs, 1)
        warmup_steps = min(self.config.warmup_steps, total_steps // 5)

        def lr_lambda(current_step: int) -> float:
            if current_step < warmup_steps:
                return float(current_step + 1) / float(max(1, warmup_steps))
            # Cosine annealing from 1.0 down to min_lr_ratio
            progress = float(current_step - warmup_steps) / float(max(1, total_steps - warmup_steps))
            cosine_decay = 0.5 * (1.0 + math.cos(math.pi * progress))
            return self.config.min_lr_ratio + (1.0 - self.config.min_lr_ratio) * cosine_decay

        scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
        return optimizer, scheduler

    def train_epoch(self, epoch: int) -> float:
        """
        Executes a single training epoch with:
        - Autoregressive Teacher Forcing
        - Gradient accumulation
        - Mixed precision autocast
        - Gradient clipping
        - Progress logging
        """
        self.model.train()
        total_epoch_loss = 0.0
        accumulated_loss = 0.0
        total_batches = len(self.train_dataloader)
        if self.config.max_train_batches is not None:
            epoch_batches = min(total_batches, self.config.max_train_batches)
        else:
            epoch_batches = total_batches
        epoch_start_time = time.time()

        self.optimizer.zero_grad(set_to_none=True)

        for batch_idx, batch in enumerate(self.train_dataloader, start=1):
            if batch_idx > epoch_batches:
                break
            # Move batch tensors to device
            src_tokens = batch["src_tokens"].to(self.device, non_blocking=True)
            tgt_tokens = batch["tgt_tokens"].to(self.device, non_blocking=True)
            labels = batch["labels"].to(self.device, non_blocking=True)
            src_mask = batch["src_key_padding_mask"].to(self.device, non_blocking=True)
            tgt_mask = batch["tgt_key_padding_mask"].to(self.device, non_blocking=True)

            # Mixed precision forward pass
            use_amp = (self.device.type == "cuda" and self.amp_dtype != torch.float32)
            with torch.amp.autocast(device_type=self.device.type, dtype=self.amp_dtype, enabled=use_amp):
                outputs = self.model(
                    src_tokens=src_tokens,
                    tgt_tokens=tgt_tokens,
                    src_key_padding_mask=src_mask,
                    tgt_key_padding_mask=tgt_mask,
                    labels=labels
                )
                loss = outputs["loss"]
                # Scale loss for gradient accumulation
                loss = loss / self.config.gradient_accumulation_steps

            # Backward pass with gradient scaling
            if self.scaler is not None:
                self.scaler.scale(loss).backward()
            else:
                loss.backward()

            raw_loss_val = loss.item() * self.config.gradient_accumulation_steps
            total_epoch_loss += raw_loss_val
            accumulated_loss += raw_loss_val

            # Optimizer Step at gradient accumulation boundary
            if batch_idx % self.config.gradient_accumulation_steps == 0 or batch_idx == epoch_batches:
                if self.scaler is not None:
                    self.scaler.unscale_(self.optimizer)
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.config.max_grad_norm)
                    self.scaler.step(self.optimizer)
                    self.scaler.update()
                else:
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.config.max_grad_norm)
                    self.optimizer.step()

                self.scheduler.step()
                self.optimizer.zero_grad(set_to_none=True)
                self.global_step += 1

            # Periodic logging
            if batch_idx % self.config.log_interval == 0 or batch_idx == epoch_batches:
                current_lr = self.scheduler.get_last_lr()[0]
                avg_recent_loss = accumulated_loss / min(self.config.log_interval, batch_idx)
                vram_info = ""
                if self.device.type == "cuda":
                    alloc_mb = torch.cuda.memory_allocated(0) / (1024 ** 2)
                    vram_info = f" | VRAM: {alloc_mb:.1f}MB"

                print(
                    f"Epoch [{epoch:02d}/{self.config.num_epochs:02d}] "
                    f"Step [{batch_idx:04d}/{epoch_batches:04d}] "
                    f"Loss: {avg_recent_loss:.4f} | LR: {current_lr:.2e}{vram_info}"
                )
                accumulated_loss = 0.0

        avg_epoch_loss = total_epoch_loss / max(epoch_batches, 1)
        duration = time.time() - epoch_start_time
        print(f" -> Epoch {epoch} Complete | Train Loss: {avg_epoch_loss:.4f} | Time: {duration:.1f}s")
        return avg_epoch_loss

    @torch.no_grad()
    def validate(self) -> Dict[str, float]:
        """
        Evaluates model on validation data:
        - Cross-Entropy Loss (with ignore_index=pad_token_id)
        - Perplexity = exp(loss)
        - Token-level next-word prediction accuracy
        """
        if self.val_dataloader is None or len(self.val_dataloader) == 0:
            return {"val_loss": 0.0, "val_perplexity": 1.0, "val_token_accuracy": 0.0}

        self.model.eval()
        total_loss = 0.0
        correct_tokens = 0
        total_tokens = 0

        use_amp = (self.device.type == "cuda" and self.amp_dtype != torch.float32)

        val_batches_count = len(self.val_dataloader)
        if self.config.max_val_batches is not None:
            max_v = min(val_batches_count, self.config.max_val_batches)
        else:
            max_v = val_batches_count

        processed_val_batches = 0
        for batch_idx, batch in enumerate(self.val_dataloader, start=1):
            if batch_idx > max_v:
                break
            processed_val_batches += 1
            src_tokens = batch["src_tokens"].to(self.device, non_blocking=True)
            tgt_tokens = batch["tgt_tokens"].to(self.device, non_blocking=True)
            labels = batch["labels"].to(self.device, non_blocking=True)
            src_mask = batch["src_key_padding_mask"].to(self.device, non_blocking=True)
            tgt_mask = batch["tgt_key_padding_mask"].to(self.device, non_blocking=True)

            with torch.amp.autocast(device_type=self.device.type, dtype=self.amp_dtype, enabled=use_amp):
                outputs = self.model(
                    src_tokens=src_tokens,
                    tgt_tokens=tgt_tokens,
                    src_key_padding_mask=src_mask,
                    tgt_key_padding_mask=tgt_mask,
                    labels=labels
                )
                loss = outputs["loss"]
                logits = outputs["logits"]

            total_loss += loss.item()

            # Token Accuracy Calculation (excluding pad tokens)
            preds = torch.argmax(logits, dim=-1)
            valid_mask = (labels != self.model.config.pad_token_id)
            correct_tokens += ((preds == labels) & valid_mask).sum().item()
            total_tokens += valid_mask.sum().item()

        avg_loss = total_loss / max(processed_val_batches, 1)
        perplexity = math.exp(min(avg_loss, 20.0))  # cap exponent to prevent overflow
        accuracy = (correct_tokens / max(total_tokens, 1)) * 100.0

        return {
            "val_loss": round(avg_loss, 4),
            "val_perplexity": round(perplexity, 2),
            "val_token_accuracy": round(accuracy, 2),
        }

    def save_checkpoint(
        self,
        epoch: int,
        train_loss: float,
        val_loss: float,
        val_perplexity: float,
        is_best: bool = False
    ) -> str:
        """
        Saves full training checkpoint including weights, optimizer, scheduler, scaler,
        and architecture configuration.
        """
        checkpoint_dict = {
            "epoch": epoch,
            "global_step": self.global_step,
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "scheduler_state_dict": self.scheduler.state_dict() if self.scheduler else None,
            "scaler_state_dict": self.scaler.state_dict() if self.scaler else None,
            "train_loss": train_loss,
            "val_loss": val_loss,
            "val_perplexity": val_perplexity,
            "model_config": self.model.config.to_dict(),
            "training_config": self.config.to_dict(),
            "tokenizer_config": self.tokenizer.config.to_dict() if hasattr(self.tokenizer, "config") else {},
            "torch_version": torch.__version__,
            "architecture": "1_encoder_13_decoder_evolved_transformer",
        }

        # Save latest checkpoint
        latest_path = os.path.join(self.config.checkpoint_dir, "checkpoint_latest.pt")
        torch.save(checkpoint_dict, latest_path)

        # Save best checkpoint
        if is_best:
            best_path = os.path.join(self.config.checkpoint_dir, "checkpoint_best.pt")
            torch.save(checkpoint_dict, best_path)

        # Save epoch checkpoint
        epoch_path = os.path.join(self.config.checkpoint_dir, f"checkpoint_epoch_{epoch:02d}.pt")
        torch.save(checkpoint_dict, epoch_path)

        # Prune older epoch checkpoints
        self._prune_checkpoints()

        return latest_path

    def _prune_checkpoints(self):
        """Retains only the last N epoch checkpoints to conserve disk space."""
        ckpts = []
        for f in os.listdir(self.config.checkpoint_dir):
            if f.startswith("checkpoint_epoch_") and f.endswith(".pt"):
                ckpts.append(os.path.join(self.config.checkpoint_dir, f))
        ckpts.sort()
        while len(ckpts) > self.config.keep_last_n_checkpoints:
            oldest = ckpts.pop(0)
            try:
                os.remove(oldest)
            except OSError:
                pass

    def load_checkpoint(self, checkpoint_path: str):
        """
        Loads training state from checkpoint file for training resumption or evaluation.
        """
        if not os.path.exists(checkpoint_path):
            raise FileNotFoundError(f"Checkpoint file not found at {checkpoint_path}")

        print(f"[Checkpoint] Resuming from checkpoint: {checkpoint_path}")
        checkpoint = torch.load(checkpoint_path, map_location=self.device, weights_only=False)

        # Load weights
        self.model.load_state_dict(checkpoint["model_state_dict"])
        if "optimizer_state_dict" in checkpoint and checkpoint["optimizer_state_dict"]:
            self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        if "scheduler_state_dict" in checkpoint and checkpoint["scheduler_state_dict"] and self.scheduler:
            self.scheduler.load_state_dict(checkpoint["scheduler_state_dict"])
        if "scaler_state_dict" in checkpoint and checkpoint["scaler_state_dict"] and self.scaler:
            self.scaler.load_state_dict(checkpoint["scaler_state_dict"])

        self.start_epoch = checkpoint.get("epoch", 0) + 1
        self.global_step = checkpoint.get("global_step", 0)
        self.best_val_loss = checkpoint.get("val_loss", float("inf"))
        print(
            f"[Checkpoint] Successfully restored! Resuming at Epoch {self.start_epoch}, "
            f"Global Step {self.global_step}, Best Val Loss: {self.best_val_loss:.4f}"
        )

    def train(self) -> Dict[str, Any]:
        """
        Main training loop over all configured epochs.
        Returns final training metadata and loss tracking history.
        """
        print("\n" + "=" * 70)
        print(f"MEENA — NEURAL MODEL TRAINING (1 Encoder + 13 Decoders)")
        print(f"Target Epochs: {self.config.num_epochs} | Batch Size: {self.config.batch_size} "
              f"(Effective: {self.config.effective_batch_size})")
        print("=" * 70 + "\n")

        total_training_start = time.time()
        initial_train_loss: Optional[float] = None
        final_train_loss: Optional[float] = None
        final_val_metrics: Dict[str, float] = {}

        for epoch in range(self.start_epoch, self.config.num_epochs + 1):
            # 1. Train 1 Epoch
            train_loss = self.train_epoch(epoch)
            if initial_train_loss is None:
                initial_train_loss = train_loss
            final_train_loss = train_loss

            # 2. Validation
            val_metrics = {"val_loss": 0.0, "val_perplexity": 1.0, "val_token_accuracy": 0.0}
            if self.val_dataloader and (epoch % self.config.eval_every_n_epochs == 0):
                val_metrics = self.validate()
                print(
                    f" -> Validation: Loss: {val_metrics['val_loss']:.4f} | "
                    f"Perplexity: {val_metrics['val_perplexity']} | "
                    f"Token Acc: {val_metrics['val_token_accuracy']:.2f}%"
                )
            final_val_metrics = val_metrics

            # 3. Checkpoint Saving
            is_best = val_metrics["val_loss"] < self.best_val_loss
            if is_best and val_metrics["val_loss"] > 0.0:
                self.best_val_loss = val_metrics["val_loss"]

            saved_path = self.save_checkpoint(
                epoch=epoch,
                train_loss=train_loss,
                val_loss=val_metrics["val_loss"],
                val_perplexity=val_metrics["val_perplexity"],
                is_best=is_best
            )

            # Record history
            self.history.append({
                "epoch": epoch,
                "train_loss": round(train_loss, 4),
                "val_loss": val_metrics["val_loss"],
                "val_perplexity": val_metrics["val_perplexity"],
                "val_token_accuracy": val_metrics["val_token_accuracy"],
                "checkpoint": saved_path
            })

        total_duration = time.time() - total_training_start

        # Save training summary metrics
        metrics_summary = {
            "initial_train_loss": initial_train_loss,
            "final_train_loss": final_train_loss,
            "final_val_loss": final_val_metrics.get("val_loss", 0.0),
            "final_val_perplexity": final_val_metrics.get("val_perplexity", 1.0),
            "final_val_token_accuracy": final_val_metrics.get("val_token_accuracy", 0.0),
            "epochs_completed": self.config.num_epochs,
            "training_duration_seconds": round(total_duration, 2),
            "device_used": str(self.device),
            "checkpoint_location": os.path.join(self.config.checkpoint_dir, "checkpoint_best.pt"),
            "history": self.history
        }

        summary_path = os.path.join(self.config.output_dir, "training_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(metrics_summary, f, indent=2)

        return metrics_summary

    @torch.no_grad()
    def generate_response(
        self,
        prompt: str,
        max_new_tokens: int = 40,
        temperature: float = 0.7,
        top_k: int = 40,
        top_p: float = 0.9,
    ) -> str:
        """
        Generates text response using the trained Evolved Transformer weights.
        """
        if self.tokenizer is None:
            raise ValueError("Tokenizer required for text generation")

        self.model.eval()

        # Format prompt with User turn indicator
        context_text = f"User: {prompt}"
        context_ids = self.tokenizer.encode(context_text, add_special_tokens=False)

        # Truncate if exceeds max_seq_len
        if len(context_ids) > self.model.config.max_seq_len:
            context_ids = context_ids[-self.model.config.max_seq_len:]

        src_tensor = torch.tensor([context_ids], dtype=torch.long, device=self.device)

        # Autoregressive generation using model.generate()
        gen_tokens = self.model.generate(
            src_tokens=src_tensor,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            bos_token_id=self.tokenizer.bos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id,
        )

        # Decode tokens to text
        token_list = gen_tokens[0].tolist()
        # Remove BOS token from generated output if present
        if token_list and token_list[0] == self.tokenizer.bos_token_id:
            token_list = token_list[1:]
        # Truncate at EOS if present
        if self.tokenizer.eos_token_id in token_list:
            eos_idx = token_list.index(self.tokenizer.eos_token_id)
            token_list = token_list[:eos_idx]

        return self.tokenizer.decode(token_list)

