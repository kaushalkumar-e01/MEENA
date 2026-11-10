"""
Audit script for MEENA existing training, validation, and test datasets.
"""

import json
from collections import Counter

def run_audit():
    print("=" * 60)
    print("MEENA DATASET AUDIT REPORT")
    print("=" * 60)

    splits = ['train', 'val', 'test']
    split_resps = {}

    for split in splits:
        path = f"ml-service/data/processed/{split}.jsonl"
        with open(path, "r", encoding="utf-8") as f:
            records = [json.loads(line) for line in f]

        total = len(records)
        responses = [r['response'] for r in records]
        contexts = [r['context'] for r in records]
        conv_ids = [r.get('conversation_id', '') for r in records]

        split_resps[split] = set(responses)
        unique_resp = len(set(responses))
        unique_ctx = len(set(contexts))
        unique_convs = len(set(conv_ids))

        template_count = sum(1 for c in contexts if '(Context update #' in c)
        resp_lengths = [len(r.split()) for r in responses]
        avg_resp_len = sum(resp_lengths) / max(len(resp_lengths), 1)

        print(f"\n--- Split: {split.upper()} ---")
        print(f"Total turns:                        {total}")
        print(f"Unique conversation IDs:            {unique_convs}")
        print(f"Unique target responses:            {unique_resp}")
        print(f"Unique input contexts:              {unique_ctx}")
        print(f"Synthetic '(Context update #)' tags: {template_count} ({template_count/total*100:.1f}%)")
        print(f"Average response word length:       {avg_resp_len:.1f} words")
        print("Most common responses:")
        for resp, count in Counter(responses).most_common(2):
            print(f"  [{count}x]: {resp[:65]}...")

    train_resps = split_resps['train']
    val_resps = split_resps['val']
    test_resps = split_resps['test']

    val_in_train = len(val_resps.intersection(train_resps))
    test_in_train = len(test_resps.intersection(train_resps))

    print("\n" + "=" * 60)
    print("CROSS-SPLIT TARGET LEAKAGE AUDIT")
    print("=" * 60)
    print(f"Val responses in Train:  {val_in_train} / {len(val_resps)} ({val_in_train/max(len(val_resps),1)*100:.1f}%)")
    print(f"Test responses in Train: {test_in_train} / {len(test_resps)} ({test_in_train/max(len(test_resps),1)*100:.1f}%)")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()

