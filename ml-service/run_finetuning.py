"""
MEENA — Task 7 Conversational Fine-Tuning Entrypoint

Fine-tunes the pretrained Evolved Transformer checkpoint (checkpoint_task7_pretrained.pt)
on MEENA's curated empathetic, mindful conversational dataset:
- Loads pretrained weights to preserve general language representations
- Uses conservative learning rate (2e-4) to avoid catastrophic forgetting
- Multi-turn dialogue formatting with clean turn delimiters
- Saves checkpoint_task7_finetuned.pt and updates checkpoint_best.pt
"""

import os
import sys
import json
import argparse
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


def run_finetuning(
    pretrained_ckpt: str = "ml-service/checkpoints/checkpoint_task7_pretrained.pt",
    epochs: int = 8,
    batch_size: int = 4,
    grad_accum: int = 4,
    lr: float = 2e-4,
    device: str = "auto",
    mixed_precision: str = "fp16"
):
    print("=" * 70)
    print("MEENA TASK 7 — CONVERSATIONAL FINE-TUNING")
    print(f"Base Pretrained Checkpoint: {pretrained_ckpt}")
    print("=" * 70)

    if not os.path.exists(pretrained_ckpt):
        raise FileNotFoundError(f"Pretrained checkpoint not found at {pretrained_ckpt}")

    # 1. Load Tokenizer
    tok_dir = os.path.join(BASE_DIR, "data", "tokenizer")
    tokenizer = MeenaTokenizer.load(tok_dir)
    print(f"[Tokenizer] Loaded Tokenizer (Vocab: {tokenizer.get_vocab_size()})")

    # 2. DataLoaders (using MEENA curated dataset)
    data_cfg = DataPipelineConfig(
        base_dir=BASE_DIR,
        processed_data_dir="data/processed",
        batch_size=batch_size,
        max_seq_len=128
    )

    train_loader = create_dataloader("train", tokenizer, data_cfg, batch_size=batch_size, shuffle=True)
    val_loader = create_dataloader("val", tokenizer, data_cfg, batch_size=batch_size, shuffle=False)
    print(f"[DataLoader] Curated Dataset: {len(train_loader)} train batches | {len(val_loader)} val batches")

    # 3. Model Architecture (Strict 1 Enc + 13 Dec)
    model_config = EvolvedTransformerConfig(
        num_encoder_layers=1,
        num_decoder_layers=13,
        d_model=128,
        n_heads=4,
        d_ff=512,
        max_seq_len=128,
        vocab_size=tokenizer.get_vocab_size(),
        pad_token_id=tokenizer.pad_token_id,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        unk_token_id=tokenizer.unk_token_id,
        use_gradient_checkpointing=True,
        mixed_precision=mixed_precision
    )

    model = MeenaEvolvedTransformer(model_config)

    # Load pretrained weights into model
    print(f"[Weights] Restoring pretrained weights from {pretrained_ckpt}...")
    ckpt = torch.load(pretrained_ckpt, map_location="cpu", weights_only=False)
    model.load_state_dict(ckpt["model_state_dict"])
    print(" -> Pretrained model state successfully loaded!")

    # 4. Trainer Configuration
    checkpoint_dir = os.path.join(BASE_DIR, "checkpoints")
    train_cfg = TrainingConfig(
        base_dir=BASE_DIR,
        batch_size=batch_size,
        gradient_accumulation_steps=grad_accum,
        learning_rate=lr,
        num_epochs=epochs,
        device=device,
        mixed_precision=mixed_precision,
        checkpoint_dir=checkpoint_dir
    )

    trainer = MeenaTrainer(
        model=model,
        config=train_cfg,
        train_dataloader=train_loader,
        val_dataloader=val_loader,
        tokenizer=tokenizer
    )

    # 5. Execute Fine-Tuning
    summary = trainer.train()

    # 6. Save Explicit Fine-Tuned Checkpoint
    finetuned_ckpt_path = os.path.join(checkpoint_dir, "checkpoint_task7_finetuned.pt")
    best_ckpt_path = os.path.join(checkpoint_dir, "checkpoint_best.pt")
    if os.path.exists(best_ckpt_path):
        import shutil
        shutil.copyfile(best_ckpt_path, finetuned_ckpt_path)
        print(f"[Persistence] Saved fine-tuned checkpoint to: {finetuned_ckpt_path}")

    summary["finetuned_checkpoint_path"] = finetuned_ckpt_path

    # Save summary report
    summary_path = os.path.join(BASE_DIR, "outputs", "task7_finetuning_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 70)
    print("TASK 7 CONVERSATIONAL FINE-TUNING COMPLETE")
    print(f" -> Finetuned Checkpoint:  {finetuned_ckpt_path}")
    print(f" -> Initial Train Loss:    {summary['initial_train_loss']:.4f}")
    print(f" -> Final Train Loss:      {summary['final_train_loss']:.4f}")
    print(f" -> Final Validation Loss: {summary['final_val_loss']:.4f}")
    print(f" -> Validation Perplexity: {summary['final_val_perplexity']:.2f}")
    print(f" -> Validation Token Acc:  {summary['final_val_token_accuracy']:.2f}%")
    print("=" * 70)

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--grad-accum", type=int, default=4)
    parser.add_argument("--lr", type=float, default=2e-4)
    args = parser.parse_args()

    run_finetuning(
        epochs=args.epochs,
        batch_size=args.batch_size,
        grad_accum=args.grad_accum,
        lr=args.lr
    )

