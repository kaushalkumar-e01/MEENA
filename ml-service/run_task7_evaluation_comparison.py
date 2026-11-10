"""
MEENA — Task 7 Four-Checkpoint Rigorous Evaluation Comparison

Compares all 4 checkpoints on the exact same 100 held-out prompts:
1. Task 4 Baseline (checkpoint_task4_best.pt)
2. Task 5 Reconstructed (checkpoint_task5_best.pt)
3. Task 7 Pretrained (checkpoint_task7_pretrained.pt)
4. Task 7 Fine-Tuned (checkpoint_task7_finetuned.pt)

Evaluates:
- 1-5 Rubric Score
- Repetition & Stuttering Rate
- Valid Word Ratio
- TF-IDF Semantic Similarity
- Multi-Turn Context Retention
- Actual Generated Responses Side-by-Side
"""

import os
import sys
import json
import time

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from meena_inference import MeenaInferenceEngine
from held_out_benchmark_data import HELD_OUT_BENCHMARK_PROMPTS
from run_semantic_benchmark import evaluate_response_semantics


def evaluate_four_checkpoints(output_path: str = "ml-service/outputs/task7_four_checkpoint_comparison.json"):
    checkpoints = {
        "task4": os.path.join(BASE_DIR, "checkpoints", "checkpoint_task4_best.pt"),
        "task5": os.path.join(BASE_DIR, "checkpoints", "checkpoint_task5_best.pt"),
        "task7_pretrain": os.path.join(BASE_DIR, "checkpoints", "checkpoint_task7_pretrained.pt"),
        "task7_finetune": os.path.join(BASE_DIR, "checkpoints", "checkpoint_task7_finetuned.pt")
    }

    for name, path in checkpoints.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"Checkpoint {name} not found at {path}")

    print("=" * 80)
    print("MEENA TASK 7 — 4-CHECKPOINT CONVERSATIONAL BENCHMARK (100 PROMPTS)")
    print("=" * 80)

    # 1. Load Engines
    engines = {}
    for name, path in checkpoints.items():
        print(f"Loading {name} ({os.path.basename(path)})...")
        engines[name] = MeenaInferenceEngine(checkpoint_path=path, device="auto", use_fp16=True)

    # 2. Run Evaluations
    print("\nRunning inference across all 100 prompts for all 4 models...")
    all_results = []
    ckpt_stats = {k: {"rubric_sum": 0.0, "rep_count": 0, "word_val_sum": 0.0, "tfidf_sum": 0.0, "ctx_sum": 0.0} for k in checkpoints}

    for idx, item in enumerate(HELD_OUT_BENCHMARK_PROMPTS, start=1):
        prompt = item["prompt"]
        cat = item["category"]
        history = item.get("history", [])

        res_item = {
            "id": item["id"],
            "category": cat,
            "prompt": prompt,
            "history": history,
            "expected_concepts": item.get("expected_concepts", []),
            "models": {}
        }

        for name, engine in engines.items():
            gen_res = engine.generate(
                prompt=prompt,
                history=history,
                max_new_tokens=45,
                temperature=0.7,
                repetition_penalty=1.35
            )
            sem = evaluate_response_semantics(
                item,
                gen_res.get("raw_generated", ""),
                gen_res["response"],
                gen_res.get("is_fallback", False)
            )

            res_item["models"][name] = {
                "raw_generated": gen_res.get("raw_generated", ""),
                "clean_response": gen_res["response"],
                "is_fallback": gen_res.get("is_fallback", False),
                "semantics": sem
            }

            s = ckpt_stats[name]
            s["rubric_sum"] += sem["rubric_score_1_to_5"]
            if sem["is_repetitive"]: s["rep_count"] += 1
            s["word_val_sum"] += sem["valid_word_ratio"]
            s["tfidf_sum"] += sem["tfidf_semantic_similarity"]
            s["ctx_sum"] += sem["context_retention_score"]

        all_results.append(res_item)
        if idx % 20 == 0 or idx == len(HELD_OUT_BENCHMARK_PROMPTS):
            print(f"  Processed {idx}/100 prompts...")

    n = len(all_results)
    summary_metrics = {}
    for name, s in ckpt_stats.items():
        summary_metrics[name] = {
            "avg_rubric_score_1_to_5": round(s["rubric_sum"] / n, 2),
            "repetitive_outputs_count": s["rep_count"],
            "repetitive_percentage": round(s["rep_count"] / n * 100, 1),
            "avg_valid_word_ratio": round(s["word_val_sum"] / n, 3),
            "avg_tfidf_semantic_sim": round(s["tfidf_sum"] / n, 3),
            "avg_context_retention_score": round(s["ctx_sum"] / 10, 3)  # 10 multi-turn prompts
        }

    final_report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_prompts": n,
        "summary_metrics": summary_metrics,
        "checkpoints_evaluated": {k: os.path.basename(v) for k, v in checkpoints.items()},
        "results": all_results
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("TASK 7 FOUR-CHECKPOINT COMPARISON COMPLETE")
    print("=" * 80)
    for name, m in summary_metrics.items():
        print(f"[{name.upper():16}] Rubric: {m['avg_rubric_score_1_to_5']}/5.0 | Repetition: {m['repetitive_percentage']}% | Word Validity: {m['avg_valid_word_ratio']*100:.1f}% | TF-IDF: {m['avg_tfidf_semantic_sim']}")
    print("=" * 80)

    return final_report


if __name__ == "__main__":
    evaluate_four_checkpoints()

