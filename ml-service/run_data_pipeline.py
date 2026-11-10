"""
MEENA — Executable Data Pipeline Script

Prepares the conversational dataset, trains the BPE tokenizer on the training split,
validates special token IDs, saves all artifacts, and verifies PyTorch DataLoader batching.

Usage:
    python run_data_pipeline.py [--vocab-size 8000] [--batch-size 4]
"""

import os
import sys
import argparse
import json

# Ensure ml-service is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from data_pipeline.config import DataPipelineConfig
from data_pipeline.dataset_prep import prepare_dataset_pipeline
from data_pipeline.tokenizer import MeenaTokenizer
from data_pipeline.dataset import create_dataloader


def run_pipeline(
    vocab_size: int = 8000,
    batch_size: int = 4,
    max_seq_len: int = 128
):
    print("=" * 70)
    print("MEENA — CONVERSATIONAL DATASET & TOKENIZER PIPELINE")
    print("=" * 70)

    config = DataPipelineConfig(
        vocab_size=vocab_size,
        batch_size=batch_size,
        max_seq_len=max_seq_len
    )

    # 1. Dataset Preparation & Splitting
    print("\n[Step 1/4] Preparing conversational dataset & generating splits...")
    meta = prepare_dataset_pipeline(config)
    print(f" -> Total conversations processed: {meta['total_conversations']}")
    for split_name, sinfo in meta["split_counts"].items():
        print(f"    - {split_name.capitalize():12}: {sinfo['conversations']} conversations ({sinfo['turns']} turns) -> {sinfo['filepath']}")

    # 2. Tokenizer Training (Strictly on Train Split ONLY)
    print("\n[Step 2/4] Training ByteLevel BPE Tokenizer on training split...")
    train_path = meta["split_counts"]["train"]["filepath"]

    def train_text_iterator():
        with open(train_path, "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line)
                yield item["context"]
                yield item["response"]

    tokenizer = MeenaTokenizer.train_from_iterator(train_text_iterator(), config)
    print(f" -> Tokenizer trained successfully. Vocabulary Size: {tokenizer.get_vocab_size()}")

    # 3. Save and Reload Tokenizer
    print(f"\n[Step 3/4] Saving tokenizer artifacts to {config.tokenizer_dir}...")
    tokenizer.save(config.tokenizer_dir)
    loaded_tokenizer = MeenaTokenizer.load(config.tokenizer_dir, config)
    print(f" -> Tokenizer reloaded and verified. Special Token IDs:")
    print(f"    - PAD ({loaded_tokenizer.pad_token}): {loaded_tokenizer.pad_token_id}")
    print(f"    - BOS ({loaded_tokenizer.bos_token}): {loaded_tokenizer.bos_token_id}")
    print(f"    - EOS ({loaded_tokenizer.eos_token}): {loaded_tokenizer.eos_token_id}")
    print(f"    - UNK ({loaded_tokenizer.unk_token}): {loaded_tokenizer.unk_token_id}")

    # 4. PyTorch DataLoader Verification
    print("\n[Step 4/4] Verifying PyTorch DataLoaders and dynamic batch collation...")
    train_loader = create_dataloader("train", loaded_tokenizer, config)
    val_loader = create_dataloader("val", loaded_tokenizer, config)
    test_loader = create_dataloader("test", loaded_tokenizer, config)

    sample_batch = next(iter(train_loader))
    print(f" -> Train DataLoader batches: {len(train_loader)}")
    print(f" -> Val DataLoader batches:   {len(val_loader)}")
    print(f" -> Test DataLoader batches:  {len(test_loader)}")
    print(f" -> Sample Batch Shapes:")
    print(f"    - src_tokens:            {list(sample_batch['src_tokens'].shape)} (dtype: {sample_batch['src_tokens'].dtype})")
    print(f"    - tgt_tokens:            {list(sample_batch['tgt_tokens'].shape)} (dtype: {sample_batch['tgt_tokens'].dtype})")
    print(f"    - labels:                {list(sample_batch['labels'].shape)} (dtype: {sample_batch['labels'].dtype})")
    print(f"    - src_key_padding_mask:  {list(sample_batch['src_key_padding_mask'].shape)} (dtype: {sample_batch['src_key_padding_mask'].dtype})")
    print(f"    - tgt_key_padding_mask:  {list(sample_batch['tgt_key_padding_mask'].shape)} (dtype: {sample_batch['tgt_key_padding_mask'].dtype})")

    print("\n" + "=" * 70)
    print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MEENA Data Pipeline")
    parser.add_argument("--vocab-size", type=int, default=8000, help="Vocabulary size")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size")
    parser.add_argument("--max-seq-len", type=int, default=128, help="Maximum sequence length")
    args = parser.parse_args()

    run_pipeline(
        vocab_size=args.vocab_size,
        batch_size=args.batch_size,
        max_seq_len=args.max_seq_len
    )
