"""
MEENA — Large-Scale Language Pretraining Entrypoint (Task 7)

Pretrains the 1-Encoder + 13-Decoder Evolved Transformer architecture (4,330,880 parameters)
on the OpenAssistant OASST1 pretraining corpus (1.1M+ tokens):
- Preserves exact 1 enc + 13 dec blocks and 3,101-token vocabulary
- Smoke test before full pretraining
- FP16 mixed precision with GradScaler (safe for 4GB VRAM)
- Cosine annealing learning rate scheduler with warmup
- Saves checkpoint_task7_pretrained.pt
"""

import os
import sys
import time
import argparse
import json
import torch

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from meena_model.config import EvolvedTransformerConfig
from meena_model.model import MeenaEvolvedTransformer
from data_pipeline.config import DataPipelineConfig
from data_pipeline.tokenizer import MeenaTokenizer
from data_pipeline.dataset import create_dataloader
from training.config import TrainingConfig
from training.trainer import MeenaTrainer
from run_training import run_smoke_test


def run_pretraining(
    epochs: int = 4,
    batch_size: int = 8,
    grad_accum: int = 4,
    lr: float = 6e-4,
    device: str = "auto",
    mixed_precision: str = "fp16",
    max_train_batches: int = None
):
    print("=" * 70)
    print("MEENA TASK 7 — LARGE-SCALE LANGUAGE PRETRAINING (OASST1)")
    print("=" * 70)

    pretrain_data_dir = os.path.join(BASE_DIR, "data", "pretraining")
    train_file = os.path.join(pretrain_data_dir, "train.jsonl")
    val_file = os.path.join(pretrain_data_dir, "val.jsonl")

    if not (os.path.exists(train_file) and os.path.exists(val_file)):
        raise FileNotFoundError(f"Pretraining splits not found in {pretrain_data_dir}")

    # 1. Load Tokenizer
    tok_dir = os.path.join(BASE_DIR, "data", "tokenizer")
    tokenizer = MeenaTokenizer.load(tok_dir)
    actual_vocab = tokenizer.get_vocab_size()
    print(f"[Tokenizer] Loaded ByteLevel BPE Tokenizer (Vocab: {actual_vocab})")

    # 2. DataLoaders
    data_cfg = DataPipelineConfig(
        base_dir=BASE_DIR,
        processed_data_dir="data/pretraining",
        batch_size=batch_size,
        max_seq_len=128
    )

    print("[DataLoader] Creating pretraining PyTorch DataLoaders...")
    train_loader = create_dataloader("train", tokenizer, data_cfg, batch_size=batch_size, shuffle=True)
    val_loader = create_dataloader("val", tokenizer, data_cfg, batch_size=batch_size, shuffle=False)
    print(f" -> Train batches: {len(train_loader)} | Val batches: {len(val_loader)}")

    # 3. Model Architecture (Strict 1 Enc + 13 Dec Blocks)
    model_config = EvolvedTransformerConfig(
        num_encoder_layers=1,
        num_decoder_layers=13,
        d_model=128,
        n_heads=4,
        d_ff=512,
        max_seq_len=128,
        vocab_size=actual_vocab,
        pad_token_id=tokenizer.pad_token_id,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        unk_token_id=tokenizer.unk_token_id,
        use_gradient_checkpointing=True,
        mixed_precision=mixed_precision
    )

    model = MeenaEvolvedTransformer(model_config)
    params = model.count_parameters()
    print(f"[Model] Initialized 1-Enc + 13-Dec Evolved Transformer ({params['total_trainable_params']:,} params)")

    # 4. Training Configuration
    checkpoint_dir = os.path.join(BASE_DIR, "checkpoints")
    train_cfg = TrainingConfig(
        base_dir=BASE_DIR,
        batch_size=batch_size,
        gradient_accumulation_steps=grad_accum,
        learning_rate=lr,
        num_epochs=epochs,
        device=device,
        mixed_precision=mixed_precision,
        checkpoint_dir=checkpoint_dir,
        max_train_batches=max_train_batches
    )

    trainer = MeenaTrainer(
        model=model,
        config=train_cfg,
        train_dataloader=train_loader,
        val_dataloader=val_loader,
        tokenizer=tokenizer
    )

    # 5. Smoke Test
    print("\n[Verification] Running pre-flight smoke test...")
    smoke_ok = run_smoke_test(trainer, tokenizer, checkpoint_dir)
    if not smoke_ok:
        raise RuntimeError("Pre-flight smoke test failed!")
    print(" -> Smoke test passed successfully!\n")

    # 6. Execute Pretraining
    summary = trainer.train()

    # 7. Save Explicit Pretrained Checkpoint
    pretrained_ckpt_path = os.path.join(checkpoint_dir, "checkpoint_task7_pretrained.pt")
    # Copy latest to pretrained checkpoint
    latest_ckpt_path = os.path.join(checkpoint_dir, "checkpoint_latest.pt")
    if os.path.exists(latest_ckpt_path):
        import shutil
        shutil.copyfile(latest_ckpt_path, pretrained_ckpt_path)
        print(f"[Persistence] Saved pretrained checkpoint to: {pretrained_ckpt_path}")

    summary["pretrained_checkpoint_path"] = pretrained_ckpt_path

    # Save summary report
    summary_path = os.path.join(BASE_DIR, "outputs", "task7_pretraining_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 70)
    print("TASK 7 PRETRAINING COMPLETE")
    print(f" -> Pretrained Checkpoint: {pretrained_ckpt_path}")
    print(f" -> Initial Train Loss:    {summary['initial_train_loss']:.4f}")
    print(f" -> Final Train Loss:      {summary['final_train_loss']:.4f}")
    print(f" -> Final Validation Loss: {summary['final_val_loss']:.4f}")
    print(f" -> Validation Perplexity: {summary['final_val_perplexity']:.2f}")
    print(f" -> Validation Token Acc:  {summary['final_val_token_accuracy']:.2f}%")
    print("=" * 70)

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--grad-accum", type=int, default=4)
    parser.add_argument("--lr", type=float, default=6e-4)
    parser.add_argument("--max-train-batches", type=int, default=None)
    args = parser.parse_args()

    run_pretraining(
        epochs=args.epochs,
        batch_size=args.batch_size,
        grad_accum=args.grad_accum,
        lr=args.lr,
        max_train_batches=args.max_train_batches
    )

