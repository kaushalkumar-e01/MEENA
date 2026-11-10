"""
MEENA — Neural Model Training & Evaluation Entrypoint

Executes training for the 1-Encoder + 13-Decoder Evolved Transformer architecture:
- Data pipeline preparation / validation
- Tokenizer loading & verification
- Model instantiation (strict 1 enc + 13 dec layers)
- Smoke testing forward/backward/checkpoint cycle
- Full multi-epoch training with mixed precision and gradient accumulation
- Validation evaluation (Loss, Perplexity, Token Accuracy)
- Checkpoint persistence (latest, best, per-epoch)
- Unseen conversational prompt evaluation

Usage:
    python run_training.py [--smoke-test] [--epochs 5] [--batch-size 4] [--grad-accum 4]
"""

import os
import sys
import time
import argparse
import json

# Ensure ml-service root is in sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import torch
from meena_model.config import EvolvedTransformerConfig
from meena_model.model import MeenaEvolvedTransformer
from data_pipeline.config import DataPipelineConfig
from data_pipeline.tokenizer import MeenaTokenizer
from data_pipeline.dataset_prep import prepare_dataset_pipeline
from data_pipeline.dataset import create_dataloader
from training.config import TrainingConfig
from training.trainer import MeenaTrainer


# Canonical unseen evaluation prompts to test trained generation
UNSEEN_EVAL_PROMPTS = [
    "I'm feeling really stressed about my upcoming deadline.",
    "Can you explain what an API is in simple words?",
    "How do you practice active listening?",
    "What are some healthy habits to start my morning?",
    "Bonjour! Comment allez-vous aujourd'hui?",
]


def run_smoke_test(
    trainer: MeenaTrainer,
    tokenizer: MeenaTokenizer,
    checkpoint_dir: str
) -> bool:
    """
    Smoke test to verify:
    1. Forward pass computes valid cross-entropy loss
    2. Backward pass computes non-NaN, non-Inf gradients
    3. Optimizer updates parameters
    4. Checkpoint saving and loading work as expected
    """
    print("\n" + "=" * 60)
    print("RUNNING TRAINING PIPELINE SMOKE TEST")
    print("=" * 60)

    model = trainer.model
    device = trainer.device
    model.train()

    # 1. Fetch one real batch from train dataloader
    print("[Smoke Test 1/5] Fetching batch from DataLoader...")
    batch = next(iter(trainer.train_dataloader))
    src = batch["src_tokens"].to(device)
    tgt = batch["tgt_tokens"].to(device)
    labels = batch["labels"].to(device)
    src_mask = batch["src_key_padding_mask"].to(device)
    tgt_mask = batch["tgt_key_padding_mask"].to(device)
    print(f" -> Batch shapes: src={list(src.shape)}, tgt={list(tgt.shape)}, labels={list(labels.shape)}")

    # 2. Forward pass & Loss
    print("[Smoke Test 2/5] Testing forward pass & loss computation...")
    trainer.optimizer.zero_grad(set_to_none=True)
    outputs = model(
        src_tokens=src,
        tgt_tokens=tgt,
        src_key_padding_mask=src_mask,
        tgt_key_padding_mask=tgt_mask,
        labels=labels
    )
    loss = outputs["loss"]
    loss_val = loss.item()
    print(f" -> Forward pass succeeded. Initial Loss: {loss_val:.4f}")
    assert not torch.isnan(loss), "Smoke test failed: loss is NaN"
    assert not torch.isinf(loss), "Smoke test failed: loss is Inf"

    # 3. Backward pass & Gradients
    print("[Smoke Test 3/5] Testing backpropagation & gradient flow...")
    if trainer.scaler is not None:
        trainer.scaler.scale(loss).backward()
        trainer.scaler.unscale_(trainer.optimizer)
    else:
        loss.backward()

    has_grad = False
    for name, p in model.named_parameters():
        if p.requires_grad and p.grad is not None:
            has_grad = True
            assert not torch.isnan(p.grad).any(), f"NaN gradient detected in {name}"
            assert not torch.isinf(p.grad).any(), f"Inf gradient detected in {name}"
    assert has_grad, "Smoke test failed: no gradients computed"
    print(" -> Backpropagation succeeded. Gradients are healthy (zero NaNs, zero Infs).")

    # 4. Optimizer update
    print("[Smoke Test 4/5] Testing optimizer parameter update...")
    target_param = next(p for p in model.parameters() if p.requires_grad and p.grad is not None and p.grad.abs().max() > 0)
    orig_param = target_param.clone().detach()

    if trainer.scaler is not None:
        trainer.scaler.step(trainer.optimizer)
        trainer.scaler.update()
    else:
        trainer.optimizer.step()

    updated_param = target_param.detach()
    param_diff = (orig_param - updated_param).abs().max().item()
    assert param_diff > 0.0, f"Smoke test failed: optimizer did not update parameters (diff={param_diff})"
    print(f" -> Optimizer step succeeded. Max parameter delta: {param_diff:.6f}")

    # 5. Checkpoint Save & Load
    print("[Smoke Test 5/5] Testing checkpoint serialization & restoration...")
    test_ckpt_path = os.path.join(checkpoint_dir, "smoke_test_checkpoint.pt")
    torch.save({
        "epoch": 0,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": trainer.optimizer.state_dict(),
        "model_config": model.config.to_dict(),
        "train_loss": loss_val,
        "architecture": "1_encoder_13_decoder_evolved_transformer"
    }, test_ckpt_path)
    assert os.path.exists(test_ckpt_path), "Failed to save smoke test checkpoint"

    restored = torch.load(test_ckpt_path, map_location=device, weights_only=False)
    assert "model_state_dict" in restored, "Restored checkpoint missing model_state_dict"
    print(f" -> Checkpoint saved and verified ({os.path.getsize(test_ckpt_path) / 1024:.1f} KB).")

    print("\n" + "=" * 60)
    print("SMOKE TEST PASSED SUCCESSFULLY!")
    print("=" * 60 + "\n")
    return True


def main():
    parser = argparse.ArgumentParser(description="MEENA Neural Model Training")
    parser.add_argument("--smoke-test", action="store_true", help="Run quick pipeline verification")
    parser.add_argument("--epochs", type=int, default=5, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=4, help="Micro-batch size")
    parser.add_argument("--grad-accum", type=int, default=4, help="Gradient accumulation steps")
    parser.add_argument("--lr", type=float, default=5e-4, help="Peak learning rate")
    parser.add_argument("--device", type=str, default="auto", choices=["auto", "cuda", "cpu"], help="Compute device")
    parser.add_argument("--mixed-precision", type=str, default="fp16", choices=["fp16", "bf16", "fp32"], help="Precision")
    parser.add_argument("--resume", type=str, default=None, help="Path to checkpoint to resume")
    parser.add_argument("--vocab-size", type=int, default=8000, help="Vocabulary size")
    parser.add_argument("--d-model", type=int, default=128, help="Model hidden dimension")
    parser.add_argument("--max-seq-len", type=int, default=128, help="Max sequence length")
    parser.add_argument("--max-train-batches", type=int, default=None, help="Cap training batches per epoch")
    parser.add_argument("--max-val-batches", type=int, default=None, help="Cap validation batches")
    args = parser.parse_args()

    print("=" * 70)
    print("MEENA — EVOLVED TRANSFORMER TRAINING & CHECKPOINT GENERATION")
    print("=" * 70)

    # 1. Ensure Data & Tokenizer are Ready
    data_cfg = DataPipelineConfig(
        base_dir=BASE_DIR,
        vocab_size=args.vocab_size,
        max_seq_len=args.max_seq_len,
        batch_size=args.batch_size
    )

    train_jsonl = os.path.join(data_cfg.processed_data_dir, "train.jsonl")
    val_jsonl = os.path.join(data_cfg.processed_data_dir, "val.jsonl")
    if not (os.path.exists(train_jsonl) and os.path.exists(val_jsonl)):
        print("\n[Data Preparation] Processed splits not found. Preparing dataset...")
        meta = prepare_dataset_pipeline(data_cfg)
        print(f" -> Processed {meta['total_conversations']} conversations.")

    # Load or Train Tokenizer
    tok_file = os.path.join(data_cfg.tokenizer_dir, "tokenizer.json")
    if not os.path.exists(tok_file):
        print(f"\n[Tokenizer] Training BPE tokenizer on {train_jsonl}...")
        def text_gen():
            with open(train_jsonl, "r", encoding="utf-8") as f:
                for line in f:
                    item = json.loads(line)
                    yield item["context"]
                    yield item["response"]
        tokenizer = MeenaTokenizer.train_from_iterator(text_gen(), data_cfg)
        tokenizer.save(data_cfg.tokenizer_dir)
        print(f" -> Tokenizer trained & saved to {data_cfg.tokenizer_dir}")
    else:
        tokenizer = MeenaTokenizer.load(data_cfg.tokenizer_dir, data_cfg)
        print(f"\n[Tokenizer] Loaded tokenizer from {data_cfg.tokenizer_dir} (Vocab: {tokenizer.get_vocab_size()})")

    # 2. Configure & Instantiate Model (STRICT: 1 Encoder + 13 Decoders)
    actual_vocab_size = tokenizer.get_vocab_size()
    model_config = EvolvedTransformerConfig(
        num_encoder_layers=1,
        num_decoder_layers=13,
        d_model=args.d_model,
        n_heads=4,
        d_ff=512,
        max_seq_len=args.max_seq_len,
        vocab_size=actual_vocab_size,
        pad_token_id=tokenizer.pad_token_id,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        unk_token_id=tokenizer.unk_token_id,
        use_gradient_checkpointing=True,
        mixed_precision=args.mixed_precision
    )

    print("\n[Model] Instantiating MEENA Evolved Transformer...")
    model = MeenaEvolvedTransformer(model_config)
    param_counts = model.count_parameters()
    print(f" -> Encoder Blocks:  {param_counts['encoder_layer_count']} block ({param_counts['encoder_block_params']:,} params)")
    print(f" -> Decoder Blocks:  {param_counts['decoder_layer_count']} blocks ({param_counts['decoder_blocks_params']:,} params)")
    print(f" -> Shared Embeds:   {param_counts['embedding_params']:,} params")
    print(f" -> Total Trainable: {param_counts['total_trainable_params']:,} params")

    # 3. Create DataLoaders
    print("\n[DataLoader] Creating PyTorch training and validation DataLoaders...")
    train_loader = create_dataloader("train", tokenizer, data_cfg, batch_size=args.batch_size, shuffle=True)
    val_loader = create_dataloader("val", tokenizer, data_cfg, batch_size=args.batch_size, shuffle=False)
    print(f" -> Train batches: {len(train_loader)} | Val batches: {len(val_loader)}")

    # 4. Training Configuration
    training_config = TrainingConfig(
        base_dir=BASE_DIR,
        batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        num_epochs=args.epochs,
        device=args.device,
        mixed_precision=args.mixed_precision,
        resume_from_checkpoint=args.resume,
        max_train_batches=args.max_train_batches,
        max_val_batches=args.max_val_batches
    )

    # 5. Initialize Trainer
    trainer = MeenaTrainer(
        model=model,
        config=training_config,
        train_dataloader=train_loader,
        val_dataloader=val_loader,
        tokenizer=tokenizer
    )

    # 6. Execute Smoke Test if requested
    if args.smoke_test:
        run_smoke_test(trainer, tokenizer, training_config.checkpoint_dir)
        return

    # 7. Execute Training Loop
    summary = trainer.train()

    # 8. Unseen Conversational Generation Evaluation
    print("\n" + "=" * 70)
    print("EVALUATING TRAINED MODEL ON UNSEEN CONVERSATIONAL PROMPTS")
    print("=" * 70)
    for prompt in UNSEEN_EVAL_PROMPTS:
        resp = trainer.generate_response(prompt, max_new_tokens=40, temperature=0.7)
        print(f"\nUser:      {prompt}")
        print(f"MEENA:     {resp if resp.strip() else '[Generated tokens]'}")

    print("\n" + "=" * 70)
    print("TRAINING & EVALUATION COMPLETE")
    print(f" -> Initial Train Loss:    {summary['initial_train_loss']:.4f}")
    print(f" -> Final Train Loss:      {summary['final_train_loss']:.4f}")
    print(f" -> Final Validation Loss: {summary['final_val_loss']:.4f}")
    print(f" -> Validation Perplexity: {summary['final_val_perplexity']:.2f}")
    print(f" -> Token Accuracy:        {summary['final_val_token_accuracy']:.2f}%")
    print(f" -> Checkpoint Location:   {summary['checkpoint_location']}")
    print(f" -> Duration:              {summary['training_duration_seconds']:.1f}s")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

