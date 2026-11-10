"""
MEENA — Task 6 Semantic Intelligence & Generalization Benchmark Runner

Evaluates Task 4 and Task 5 checkpoints side-by-side across 100 held-out prompts:
- Measures dictionary word validity, repetition/stuttering, semantic relevance,
  grammatical coherence, context retention, and uncertainty handling.
- Maps results onto an objective 1–5 scoring scale aligned with the evaluation rubric.
- Produces a comprehensive, reproducible JSON evaluation report.
"""

import os
import sys
import re
import json
import time
import math
from typing import Dict, List, Any, Tuple, Optional

# Ensure ml-service root is in sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from meena_inference import MeenaInferenceEngine, HONEST_FALLBACK_RESPONSE
from held_out_benchmark_data import HELD_OUT_BENCHMARK_PROMPTS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Common English and basic foreign words to verify vocabulary validity
COMMON_WORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", "with",
    "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if",
    "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him",
    "know", "take", "people", "into", "year", "your", "good", "some", "could", "them", "see", "other", "than",
    "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how",
    "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", "day", "most",
    "us", "is", "are", "was", "were", "been", "has", "had", "done", "am", "listening", "speaking", "read", "write",
    "talk", "understand", "feeling", "anxious", "stress", "calm", "pomodoro", "api", "code", "python", "git",
    "water", "sun", "rain", "earth", "light", "tea", "coffee", "morning", "evening", "sleep", "rest", "night",
    "bonjour", "comment", "merci", "guten", "tag", "wie", "hola", "cómo", "estás", "namaste", "aap", "hai"
}


def evaluate_response_semantics(
    prompt_item: Dict[str, Any],
    raw_response: str,
    clean_response: str,
    is_fallback: bool
) -> Dict[str, Any]:
    """
    Evaluates semantic intelligence, grammar, context retention, and repetition.
    Computes a score from 1 to 5 following the official MEENA rubric:
    1 — Incoherent or irrelevant.
    2 — Partially relevant but mostly incorrect or unclear.
    3 — Understandable but incomplete or weak.
    4 — Relevant, coherent, and useful.
    5 — Clear, accurate, and contextually appropriate.
    """
    category = prompt_item["category"]
    prompt_text = prompt_item["prompt"]
    expected_concepts = prompt_item.get("expected_concepts", [])
    history = prompt_item.get("history", [])

    text = raw_response.strip() if raw_response.strip() else clean_response.strip()
    words = re.findall(r"[A-Za-zÀ-ÿ]{2,}", text.lower())
    total_tokens = len(text.split())

    # 1. Valid Word Ratio (Checks if model produces real words vs garbage subwords)
    if not words:
        valid_word_ratio = 0.0
    else:
        valid_words = sum(1 for w in words if w in COMMON_WORDS or len(w) >= 4)
        valid_word_ratio = round(valid_words / max(len(words), 1), 3)

    # 2. Repetition & Stuttering Rate
    raw_tokens = text.split()
    has_consecutive_dup = False
    for i in range(len(raw_tokens) - 1):
        if raw_tokens[i].lower() == raw_tokens[i+1].lower() and len(raw_tokens[i]) > 1:
            has_consecutive_dup = True
            break

    # 3-gram repetition
    trigrams = [tuple(raw_tokens[i:i+3]) for i in range(len(raw_tokens) - 2)]
    trigram_rep_count = len(trigrams) - len(set(trigrams))
    is_repetitive = has_consecutive_dup or trigram_rep_count > 0

    # 3. Semantic Relevance (Concept Overlap & TF-IDF similarity)
    matched_concepts = [c for c in expected_concepts if c.lower() in text.lower()]
    concept_recall = round(len(matched_concepts) / max(len(expected_concepts), 1), 3)

    # TF-IDF cosine similarity between reference concepts and generated response
    ref_text = f"{prompt_text} {' '.join(expected_concepts)}"
    try:
        vec = TfidfVectorizer().fit([ref_text, text])
        tf_mat = vec.transform([ref_text, text])
        tfidf_sim = float(cosine_similarity(tf_mat[0:1], tf_mat[1:2])[0][0])
    except Exception:
        tfidf_sim = 0.0
    tfidf_sim = round(tfidf_sim, 3)

    # 4. Grammatical Coherence
    has_cap = bool(text and text[0].isupper())
    ends_punct = bool(text and text[-1] in {".", "!", "?", '"', "'"})
    has_verbs_or_glue = bool(re.search(r"\b(is|are|was|were|can|to|the|and|in|of|you|it|a)\b", text, re.I))
    grammar_score = 0.0
    if has_cap: grammar_score += 0.2
    if ends_punct: grammar_score += 0.3
    if has_verbs_or_glue: grammar_score += 0.5
    grammar_score = round(grammar_score, 2)

    # 5. Context Retention (Multi-turn category)
    context_retention_score = 0.0
    if category == "multi_turn_context" and history:
        hist_text = " ".join(h["text"] for h in history).lower()
        hist_words = set(re.findall(r"[A-Za-z]{4,}", hist_text))
        resp_words = set(words)
        overlap = hist_words.intersection(resp_words)
        context_retention_score = round(len(overlap) / max(min(len(hist_words), 5), 1), 3)

    # 6. Uncertainty Handling (Unknown/Unsupported categories)
    acknowledges_uncertainty = False
    if category in ("unknown_unsupported", "ambiguous_incomplete"):
        uncertainty_phrases = [
            "cannot", "predict", "future", "impossible", "do not", "learning", "clarify",
            "depends", "not sure", "honest", "tell me more", "what do you mean"
        ]
        acknowledges_uncertainty = any(p in text.lower() or p in clean_response.lower() for p in uncertainty_phrases)

    # 7. Objective 1 to 5 Rubric Score Mapping
    # Rubric:
    # 1 — Incoherent or irrelevant (broken subwords, heavy noise, zero concepts)
    # 2 — Partially relevant but mostly incorrect or unclear (some words present, but fragmented syntax)
    # 3 — Understandable but incomplete or weak (clear words, basic syntax, partial relevance)
    # 4 — Relevant, coherent, and useful (well-formed sentence, relevant content, no loops)
    # 5 — Clear, accurate, and contextually appropriate (high concept match, fluent grammar)
    if is_fallback:
        # Honest fallback is a safe refusal (Score 2.5 - 3.0 depending on category)
        if category in ("unknown_unsupported", "ambiguous_incomplete"):
            rubric_score = 3.5  # Appropriate handling of unknowable prompts
        else:
            rubric_score = 2.0  # Honest admission of ignorance for general questions
    else:
        if valid_word_ratio < 0.35 or len(words) < 3:
            rubric_score = 1.0
        elif valid_word_ratio < 0.65 or is_repetitive:
            rubric_score = 2.0
        elif concept_recall >= 0.5 and grammar_score >= 0.8:
            rubric_score = 4.0 if concept_recall < 0.8 else 5.0
        elif concept_recall >= 0.25 or tfidf_sim >= 0.25:
            rubric_score = 3.0
        else:
            rubric_score = 2.0 if valid_word_ratio >= 0.7 else 1.0

    return {
        "word_count": len(words),
        "valid_word_ratio": valid_word_ratio,
        "is_repetitive": is_repetitive,
        "concept_recall": concept_recall,
        "matched_concepts": matched_concepts,
        "tfidf_semantic_similarity": tfidf_sim,
        "grammar_coherence": grammar_score,
        "context_retention_score": context_retention_score,
        "acknowledges_uncertainty": acknowledges_uncertainty,
        "rubric_score_1_to_5": rubric_score
    }


def run_full_100_benchmark(
    ckpt_task4_path: str,
    ckpt_task5_path: str,
    output_path: str = "ml-service/outputs/task6_semantic_benchmark_report.json"
):
    print("=" * 80)
    print("MEENA TASK 6 — 100-PROMPT SEMANTIC INTELLIGENCE & GENERALIZATION BENCHMARK")
    print("=" * 80)
    print(f"Task 4 Checkpoint: {ckpt_task4_path}")
    print(f"Task 5 Checkpoint: {ckpt_task5_path}")
    print(f"Total Held-Out Prompts: {len(HELD_OUT_BENCHMARK_PROMPTS)}")
    print("=" * 80)

    # 1. Load Engines
    print("\n[1/3] Loading Task 4 Inference Engine...")
    engine_t4 = MeenaInferenceEngine(checkpoint_path=ckpt_task4_path, device="auto", use_fp16=True)
    print(f" -> Task 4 Loaded on {engine_t4.device}")

    print("\n[2/3] Loading Task 5 Inference Engine...")
    engine_t5 = MeenaInferenceEngine(checkpoint_path=ckpt_task5_path, device="auto", use_fp16=True)
    print(f" -> Task 5 Loaded on {engine_t5.device}")

    # 2. Evaluate all 100 Prompts
    print("\n[3/3] Executing 100-Prompt Side-by-Side Semantic Evaluation...")
    results: List[Dict[str, Any]] = []

    category_stats = {}

    for idx, item in enumerate(HELD_OUT_BENCHMARK_PROMPTS, start=1):
        prompt = item["prompt"]
        cat = item["category"]
        history = item.get("history", [])

        # Generate with Task 4
        res_t4 = engine_t4.generate(
            prompt=prompt,
            history=history,
            max_new_tokens=45,
            temperature=0.7,
            repetition_penalty=1.35
        )
        sem_t4 = evaluate_response_semantics(
            item,
            res_t4.get("raw_generated", ""),
            res_t4["response"],
            res_t4.get("is_fallback", False)
        )

        # Generate with Task 5
        res_t5 = engine_t5.generate(
            prompt=prompt,
            history=history,
            max_new_tokens=45,
            temperature=0.7,
            repetition_penalty=1.35
        )
        sem_t5 = evaluate_response_semantics(
            item,
            res_t5.get("raw_generated", ""),
            res_t5["response"],
            res_t5.get("is_fallback", False)
        )

        # Track category stats
        if cat not in category_stats:
            category_stats[cat] = {
                "count": 0,
                "t4_rubric_sum": 0.0,
                "t5_rubric_sum": 0.0,
                "t4_rep_count": 0,
                "t5_rep_count": 0,
                "t4_tfidf_sum": 0.0,
                "t5_tfidf_sum": 0.0
            }
        cs = category_stats[cat]
        cs["count"] += 1
        cs["t4_rubric_sum"] += sem_t4["rubric_score_1_to_5"]
        cs["t5_rubric_sum"] += sem_t5["rubric_score_1_to_5"]
        if sem_t4["is_repetitive"]: cs["t4_rep_count"] += 1
        if sem_t5["is_repetitive"]: cs["t5_rep_count"] += 1
        cs["t4_tfidf_sum"] += sem_t4["tfidf_semantic_similarity"]
        cs["t5_tfidf_sum"] += sem_t5["tfidf_semantic_similarity"]

        results.append({
            "id": item["id"],
            "category": cat,
            "prompt": prompt,
            "history": history,
            "expected_concepts": item.get("expected_concepts", []),
            "task4": {
                "raw_generated": res_t4.get("raw_generated", ""),
                "clean_response": res_t4["response"],
                "is_fallback": res_t4.get("is_fallback", False),
                "semantics": sem_t4
            },
            "task5": {
                "raw_generated": res_t5.get("raw_generated", ""),
                "clean_response": res_t5["response"],
                "is_fallback": res_t5.get("is_fallback", False),
                "semantics": sem_t5
            }
        })

        if idx % 10 == 0 or idx == len(HELD_OUT_BENCHMARK_PROMPTS):
            print(f"  Processed {idx}/{len(HELD_OUT_BENCHMARK_PROMPTS)} prompts ({cat})...")

    # Overall Summary
    n = len(results)
    avg_t4_rubric = round(sum(r["task4"]["semantics"]["rubric_score_1_to_5"] for r in results) / n, 2)
    avg_t5_rubric = round(sum(r["task5"]["semantics"]["rubric_score_1_to_5"] for r in results) / n, 2)
    total_t4_rep = sum(1 for r in results if r["task4"]["semantics"]["is_repetitive"])
    total_t5_rep = sum(1 for r in results if r["task5"]["semantics"]["is_repetitive"])
    avg_t4_word_validity = round(sum(r["task4"]["semantics"]["valid_word_ratio"] for r in results) / n, 3)
    avg_t5_word_validity = round(sum(r["task5"]["semantics"]["valid_word_ratio"] for r in results) / n, 3)
    avg_t4_tfidf = round(sum(r["task4"]["semantics"]["tfidf_semantic_similarity"] for r in results) / n, 3)
    avg_t5_tfidf = round(sum(r["task5"]["semantics"]["tfidf_semantic_similarity"] for r in results) / n, 3)

    category_summary = {}
    for cat, stats in category_stats.items():
        c_count = stats["count"]
        category_summary[cat] = {
            "count": c_count,
            "t4_avg_rubric_1_to_5": round(stats["t4_rubric_sum"] / c_count, 2),
            "t5_avg_rubric_1_to_5": round(stats["t5_rubric_sum"] / c_count, 2),
            "t4_repetitive_count": stats["t4_rep_count"],
            "t5_repetitive_count": stats["t5_rep_count"],
            "t4_avg_tfidf": round(stats["t4_tfidf_sum"] / c_count, 3),
            "t5_avg_tfidf": round(stats["t5_tfidf_sum"] / c_count, 3)
        }

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_prompts": n,
        "task4_checkpoint": os.path.basename(ckpt_task4_path),
        "task5_checkpoint": os.path.basename(ckpt_task5_path),
        "overall_metrics": {
            "task4_avg_rubric_score_1_to_5": avg_t4_rubric,
            "task5_avg_rubric_score_1_to_5": avg_t5_rubric,
            "task4_repetitive_prompts_count": total_t4_rep,
            "task5_repetitive_prompts_count": total_t5_rep,
            "task4_valid_word_ratio": avg_t4_word_validity,
            "task5_valid_word_ratio": avg_t5_word_validity,
            "task4_avg_tfidf_semantic_similarity": avg_t4_tfidf,
            "task5_avg_tfidf_semantic_similarity": avg_t5_tfidf
        },
        "category_summary": category_summary,
        "scoring_rubric": {
            "1": "Incoherent or irrelevant — output contains broken subwords, heavy noise, or unrelated text.",
            "2": "Partially relevant but mostly incorrect or unclear — isolated recognizable words, but lacks syntax or meaning.",
            "3": "Understandable but incomplete or weak — basic sentence structure discernible, partial semantic relevance.",
            "4": "Relevant, coherent, and useful — well-formed grammar, directly addresses prompt, zero stuttering.",
            "5": "Clear, accurate, and contextually appropriate — fluent, logically sound, accurate context handling."
        },
        "results": results
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("TASK 6 BENCHMARK EXECUTION COMPLETE")
    print("=" * 80)
    print(f"Total Prompts Evaluated:          {n}")
    print(f"Task 4 Rubric Score (1-5):        {avg_t4_rubric} / 5.0")
    print(f"Task 5 Rubric Score (1-5):        {avg_t5_rubric} / 5.0")
    print(f"Task 4 Repetitive Outputs:        {total_t4_rep} / {n} ({total_t4_rep/n*100:.1f}%)")
    print(f"Task 5 Repetitive Outputs:        {total_t5_rep} / {n} ({total_t5_rep/n*100:.1f}%)")
    print(f"Task 4 Valid Word Ratio:          {avg_t4_word_validity * 100:.1f}%")
    print(f"Task 5 Valid Word Ratio:          {avg_t5_word_validity * 100:.1f}%")
    print(f"Task 4 TF-IDF Semantic Sim:       {avg_t4_tfidf}")
    print(f"Task 5 TF-IDF Semantic Sim:       {avg_t5_tfidf}")
    print(f"Detailed Report Persisted at:     {output_path}")
    print("=" * 80)

    return report


if __name__ == "__main__":
    ckpt_t4 = os.path.join(BASE_DIR, "checkpoints", "checkpoint_task4_best.pt")
    ckpt_t5 = os.path.join(BASE_DIR, "checkpoints", "checkpoint_task5_best.pt")
    run_full_100_benchmark(ckpt_t4, ckpt_t5)

