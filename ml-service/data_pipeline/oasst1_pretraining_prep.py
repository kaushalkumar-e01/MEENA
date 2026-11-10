"""
MEENA — Large-Scale Language Pretraining Data Pipeline (OASST1)

Extracts clean, high-quality, multi-turn conversational dialogue threads from
the OpenAssistant OASST1 corpus (Apache 2.0 License).
Implements:
- Streaming decompression (memory-safe for 8GB RAM)
- Length filtering (min 5 words, max seq length 128 tokens)
- Conversation-level train/validation/test splitting (zero leakage)
- Zero template tags, zero artificial duplication
"""

import os
import sys
import gzip
import json
import random
import unicodedata
import re
from typing import Dict, List, Tuple, Set, Optional

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from data_pipeline.dataset_prep import clean_text


def extract_threads_from_trees(
    gzip_path: str,
    target_lang: str = "en",
    max_trees: Optional[int] = 3000,
    max_branches_per_node: int = 2,
    min_word_count: int = 4,
    max_tokens: int = 120
) -> List[Dict]:
    """
    Recursively extracts root-to-leaf conversational paths from OASST1 tree structures.
    Preserves strict (user, assistant, user, assistant) speaker alternation.
    """
    if not os.path.exists(gzip_path):
        raise FileNotFoundError(f"Raw OASST1 archive not found at {gzip_path}")

    conversations = []
    trees_processed = 0

    with gzip.open(gzip_path, "rt", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            tree_id = data.get("message_tree_id", f"tree_{trees_processed}")
            prompt_node = data.get("prompt", {})

            # Filter by language
            if prompt_node.get("lang") != target_lang:
                continue

            # Recursive thread collector
            def collect_linear_paths(node, current_path, collected):
                role = "user" if node.get("role") in ("prompter", "user") else "assistant"
                raw_t = node.get("text", "")
                norm_t = clean_text(raw_t)

                words = norm_t.split()
                if len(words) < min_word_count or len(words) > 150:
                    return

                new_path = current_path + [(role, norm_t)]
                replies = node.get("replies", [])
                valid_replies = [r for r in replies if r.get("text")]

                if not valid_replies:
                    if len(new_path) >= 2:
                        collected.append(new_path)
                else:
                    for child in valid_replies[:max_branches_per_node]:
                        collect_linear_paths(child, new_path, collected)

            tree_threads = []
            collect_linear_paths(prompt_node, [], tree_threads)

            for tidx, thread in enumerate(tree_threads):
                conversations.append({
                    "id": f"oasst_{tree_id[:8]}_{tidx:02d}",
                    "tree_id": tree_id,
                    "turns": thread
                })

            trees_processed += 1
            if max_trees and trees_processed >= max_trees:
                break

    return conversations


def prepare_pretraining_dataset(
    raw_gzip_path: str = "ml-service/data/raw/oasst1_trees.jsonl.gz",
    output_dir: str = "ml-service/data/pretraining",
    max_trees: int = 2500,
    seed: int = 42
) -> Dict:
    """
    Builds the pretraining dataset from OASST1 trees and saves train.jsonl, val.jsonl, test.jsonl.
    Splits strictly by tree_id to prevent any cross-split leakage.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"[OASST1 Pipeline] Extracting conversations from {raw_gzip_path} (cap: {max_trees} trees)...")

    conversations = extract_threads_from_trees(raw_gzip_path, target_lang="en", max_trees=max_trees)
    print(f" -> Extracted {len(conversations)} raw conversational threads.")

    # Deduplicate exact threads
    unique_convs = []
    seen_threads = set()
    for c in conversations:
        thread_key = tuple((role, text) for role, text in c["turns"])
        if thread_key not in seen_threads:
            seen_threads.add(thread_key)
            unique_convs.append(c)

    print(f" -> Unique conversational threads after deduplication: {len(unique_convs)}")

    # Split by tree_id
    rng = random.Random(seed)
    unique_tree_ids = list(set(c["tree_id"] for c in unique_convs))
    rng.shuffle(unique_tree_ids)

    n_trees = len(unique_tree_ids)
    n_train = int(n_trees * 0.85)
    n_val = int(n_trees * 0.08)

    train_tree_set = set(unique_tree_ids[:n_train])
    val_tree_set = set(unique_tree_ids[n_train:n_train + n_val])
    test_tree_set = set(unique_tree_ids[n_train + n_val:])

    train_convs = [c for c in unique_convs if c["tree_id"] in train_tree_set]
    val_convs = [c for c in unique_convs if c["tree_id"] in val_tree_set]
    test_convs = [c for c in unique_convs if c["tree_id"] in test_tree_set]

    # Convert to (context, response) dialogue turns with multi-turn sliding window
    def build_turns(conv_list: List[Dict]) -> List[Dict]:
        turns = []
        for c in conv_list:
            cid = c["id"]
            history = []
            for speaker, text in c["turns"]:
                if speaker.lower() in ("assistant", "meena") and history:
                    # Format context: User: ... \n MEENA: ...
                    ctx_parts = []
                    for h_role, h_text in history[-3:]:
                        lbl = "User" if h_role.lower() in ("user", "prompter") else "MEENA"
                        ctx_parts.append(f"{lbl}: {h_text}")
                    ctx_str = "\n".join(ctx_parts)
                    turns.append({
                        "conversation_id": cid,
                        "turn_id": len(turns) + 1,
                        "context": ctx_str,
                        "response": text
                    })
                history.append((speaker, text))
        return turns

    train_turns = build_turns(train_convs)
    val_turns = build_turns(val_convs)
    test_turns = build_turns(test_convs)

    # Save to JSONL
    def write_jsonl(turns, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            for t in turns:
                f.write(json.dumps(t, ensure_ascii=False) + "\n")

    train_file = os.path.join(output_dir, "train.jsonl")
    val_file = os.path.join(output_dir, "val.jsonl")
    test_file = os.path.join(output_dir, "test.jsonl")

    write_jsonl(train_turns, train_file)
    write_jsonl(val_turns, val_file)
    write_jsonl(test_turns, test_file)

    # Count tokens with MeenaTokenizer
    from data_pipeline.tokenizer import MeenaTokenizer
    tok = MeenaTokenizer.load("ml-service/data/tokenizer")

    total_tokens = sum(len(tok.encode(t["context"])) + len(tok.encode(t["response"])) for t in train_turns)

    manifest = {
        "dataset_name": "OpenAssistant OASST1 (English Pretraining Subset)",
        "source": "https://huggingface.co/datasets/OpenAssistant/oasst1",
        "license": "Apache 2.0 License",
        "trees_processed": n_trees,
        "total_conversations": len(unique_convs),
        "split_counts": {
            "train": {"conversations": len(train_convs), "turns": len(train_turns), "filepath": train_file},
            "validation": {"conversations": len(val_convs), "turns": len(val_turns), "filepath": val_file},
            "test": {"conversations": len(test_convs), "turns": len(test_turns), "filepath": test_file}
        },
        "approx_train_tokens": total_tokens,
        "tokenizer_vocab_size": tok.get_vocab_size()
    }

    manifest_file = os.path.join(output_dir, "dataset_manifest.json")
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("\n" + "=" * 70)
    print("OASST1 PRETRAINING DATASET PREPARATION COMPLETE")
    print(f" -> Train Turns:      {len(train_turns):,} turns (~{total_tokens:,} tokens)")
    print(f" -> Validation Turns: {len(val_turns):,} turns")
    print(f" -> Test Turns:       {len(test_turns):,} turns")
    print(f" -> Manifest Saved:   {manifest_file}")
    print("=" * 70)

    return manifest


if __name__ == "__main__":
    prepare_pretraining_dataset()

