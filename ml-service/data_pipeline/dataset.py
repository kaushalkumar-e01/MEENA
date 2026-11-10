"""
MEENA — PyTorch Conversational Dataset & Dynamic Collation Pipeline

Implements memory-efficient PyTorch Dataset, Dynamic Batch Collation,
and Autoregressive Sequence-to-Sequence shifting (Teacher Forcing) for the
MEENA Evolved Transformer.
"""

import os
import json
import torch
from torch.utils.data import Dataset, DataLoader
from typing import List, Dict, Optional, Tuple, Any

from .config import DataPipelineConfig
from .tokenizer import MeenaTokenizer


class MeenaConversationalDataset(Dataset):
    """
    PyTorch Dataset for multi-turn conversational turns.
    Loads JSONL records efficiently and tokenizes on the fly to conserve system RAM.
    """
    def __init__(
        self,
        jsonl_path: str,
        tokenizer: MeenaTokenizer,
        max_seq_len: int = 128
    ):
        super().__init__()
        if not os.path.exists(jsonl_path):
            raise FileNotFoundError(f"Dataset file not found at {jsonl_path}")

        self.jsonl_path = jsonl_path
        self.tokenizer = tokenizer
        self.max_seq_len = max_seq_len

        # Read line offsets for memory-efficient random access
        self.records: List[Dict[str, str]] = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    data = json.loads(line)
                    self.records.append({
                        "context": data["context"],
                        "response": data["response"],
                        "conversation_id": data.get("conversation_id", "")
                    })

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        item = self.records[idx]
        context_text = item["context"]
        response_text = item["response"]

        # Tokenize context and response without special tokens (collate_fn handles wrapping)
        context_ids = self.tokenizer.encode(context_text, add_special_tokens=False)
        response_ids = self.tokenizer.encode(response_text, add_special_tokens=False)

        # Truncate context to max_seq_len
        if len(context_ids) > self.max_seq_len:
            context_ids = context_ids[-self.max_seq_len:]  # keep most recent context turns

        # Truncate response to max_seq_len - 1 (leave room for BOS or EOS)
        if len(response_ids) > (self.max_seq_len - 1):
            response_ids = response_ids[:(self.max_seq_len - 1)]

        return {
            "context_ids": context_ids,
            "response_ids": response_ids,
            "conversation_id": item["conversation_id"]
        }


class MeenaCollateFn:
    """
    Dynamic Batch Collation for Seq2Seq Evolved Transformer models:
    - Dynamically pads batch sequences to the max length in that specific batch.
    - Constructs Teacher-Forcing inputs:
        Decoder input:  [<bos>, r_1, r_2, ..., r_k]
        Decoder target: [r_1, r_2, ..., r_k, <eos>]
    - Generates strict boolean key padding masks:
        True indicates padding position to ignore.
    - Fully compatible with `MeenaEvolvedTransformer.forward(**batch)`.
    """
    def __init__(self, tokenizer: MeenaTokenizer, max_seq_len: int = 128):
        self.tokenizer = tokenizer
        self.max_seq_len = max_seq_len
        self.pad_id = tokenizer.pad_token_id
        self.bos_id = tokenizer.bos_token_id
        self.eos_id = tokenizer.eos_token_id

    def __call__(self, batch: List[Dict[str, Any]]) -> Dict[str, torch.Tensor]:
        batch_size = len(batch)
        if batch_size == 0:
            raise ValueError("CollateFn received an empty batch")

        # 1. Prepare Encoder Inputs (Context)
        src_sequences = [item["context_ids"] for item in batch]
        max_src_len = max(len(seq) for seq in src_sequences)
        max_src_len = max(max_src_len, 1)  # ensure at least length 1

        src_tokens = torch.full((batch_size, max_src_len), self.pad_id, dtype=torch.long)
        for i, seq in enumerate(src_sequences):
            if seq:
                src_tokens[i, :len(seq)] = torch.tensor(seq, dtype=torch.long)

        src_key_padding_mask = (src_tokens == self.pad_id)

        # 2. Prepare Decoder Inputs & Shifted Target Labels (Teacher Forcing)
        # For a response [r_1, ..., r_k]:
        # Decoder Input:  [<bos>, r_1, ..., r_k]
        # Target Label:   [r_1, ..., r_k, <eos>]
        tgt_in_sequences = []
        label_sequences = []

        for item in batch:
            resp = item["response_ids"]
            tgt_in = [self.bos_id] + resp
            lbl = resp + [self.eos_id]
            tgt_in_sequences.append(tgt_in)
            label_sequences.append(lbl)

        max_tgt_len = max(len(seq) for seq in tgt_in_sequences)
        max_tgt_len = max(max_tgt_len, 1)

        tgt_tokens = torch.full((batch_size, max_tgt_len), self.pad_id, dtype=torch.long)
        labels = torch.full((batch_size, max_tgt_len), self.pad_id, dtype=torch.long)

        for i in range(batch_size):
            seq_len = len(tgt_in_sequences[i])
            tgt_tokens[i, :seq_len] = torch.tensor(tgt_in_sequences[i], dtype=torch.long)
            labels[i, :seq_len] = torch.tensor(label_sequences[i], dtype=torch.long)

        tgt_key_padding_mask = (tgt_tokens == self.pad_id)

        return {
            "src_tokens": src_tokens,
            "tgt_tokens": tgt_tokens,
            "labels": labels,
            "src_key_padding_mask": src_key_padding_mask,
            "tgt_key_padding_mask": tgt_key_padding_mask
        }


def create_dataloader(
    split: str,
    tokenizer: MeenaTokenizer,
    config: Optional[DataPipelineConfig] = None,
    batch_size: Optional[int] = None,
    shuffle: Optional[bool] = None
) -> DataLoader:
    """
    Factory creating a PyTorch DataLoader for train, val, or test splits.
    """
    cfg = config or DataPipelineConfig()
    filename = f"{split}.jsonl"
    jsonl_path = os.path.join(cfg.processed_data_dir, filename)

    if not os.path.exists(jsonl_path):
        raise FileNotFoundError(
            f"Processed data file {jsonl_path} does not exist. "
            "Please run prepare_dataset_pipeline() first."
        )

    dataset = MeenaConversationalDataset(
        jsonl_path=jsonl_path,
        tokenizer=tokenizer,
        max_seq_len=cfg.max_seq_len
    )

    bsz = batch_size if batch_size is not None else cfg.batch_size
    do_shuffle = shuffle if shuffle is not None else (split == "train")
    collate_fn = MeenaCollateFn(tokenizer=tokenizer, max_seq_len=cfg.max_seq_len)

    return DataLoader(
        dataset=dataset,
        batch_size=bsz,
        shuffle=do_shuffle,
        collate_fn=collate_fn,
        num_workers=cfg.num_workers,
        pin_memory=cfg.pin_memory
    )
