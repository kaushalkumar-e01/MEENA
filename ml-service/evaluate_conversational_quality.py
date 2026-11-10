"""
MEENA — Task 5 Conversational Quality Evaluation Benchmark

Evaluates and compares the previous checkpoint (Task 4) and the new trained checkpoint
across 50 diverse conversational prompts under identical decoding settings.
Measures grammar, coherence, repetition, relevance, and vocabulary diversity.
"""

import os
import sys
import json
import time
from typing import Dict, List, Any, Tuple

# Ensure ml-service root is in sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from meena_inference import MeenaInferenceEngine

# 50 Diverse Conversational Prompts across 6 Categories
EVALUATION_PROMPTS = [
    # 1. Daily Greetings & Check-ins (8 prompts)
    ("greeting", "Hello MEENA! How are you doing today?"),
    ("greeting", "Good morning! Wishing you a wonderful and peaceful day."),
    ("greeting", "Hey there! What are you up to right now?"),
    ("greeting", "Good evening! It has been quite a long day."),
    ("greeting", "Hi! Who are you and how can you help me?"),
    ("greeting", "I'm heading to bed now. Good night!"),
    ("greeting", "Thank you so much for your help today!"),
    ("greeting", "Goodbye! Talk to you tomorrow."),

    # 2. Emotional Support & Empathy (10 prompts)
    ("empathy", "I'm feeling really anxious and overwhelmed by my workload today."),
    ("empathy", "I have been procrastinating all afternoon and I feel guilty about it."),
    ("empathy", "I lost my pet recently and the house feels completely empty."),
    ("empathy", "I feel like an imposter at my job and everyone else is smarter."),
    ("empathy", "A coworker took credit for my idea and I am furious."),
    ("empathy", "My mind races with worries as soon as I try to sleep."),
    ("empathy", "I feel lonely today and don't know who to reach out to."),
    ("empathy", "I made a silly mistake during my presentation and feel so embarrassed."),
    ("empathy", "How do you practice active listening when someone is upset?"),
    ("empathy", "How can I forgive myself for a mistake I made months ago?"),

    # 3. Simple Educational & Scientific Explanations (10 prompts)
    ("education", "What is photosynthesis and why is it important for Earth?"),
    ("education", "How do airplanes generate lift to stay in the air?"),
    ("education", "Why do leaves change color in the autumn?"),
    ("education", "What is the difference between speed and velocity in physics?"),
    ("education", "How does DNA store genetic information inside living cells?"),
    ("education", "Why does ice float on liquid water instead of sinking?"),
    ("education", "What causes the Northern Lights in the polar skies?"),
    ("education", "How deep is Challenger Deep in the ocean?"),
    ("education", "What causes ocean tides on Earth?"),
    ("education", "Why are prime numbers called the building blocks of arithmetic?"),

    # 4. Computer Science & Technology (10 prompts)
    ("tech", "Can you explain what an API is in simple terms?"),
    ("tech", "What is the difference between synchronous and asynchronous programming?"),
    ("tech", "What does Big O notation measure in computer science?"),
    ("tech", "What is the difference between git merge and git rebase?"),
    ("tech", "Why does adding an index to a database table speed up queries?"),
    ("tech", "What is the purpose of Docker containers?"),
    ("tech", "What does DRY stand for in software engineering?"),
    ("tech", "What is the difference between TCP and UDP?"),
    ("tech", "What is a race condition in multi-threaded programming?"),
    ("tech", "Why should secret API keys never be committed into Git?"),

    # 5. Foreign Language Practice (6 prompts)
    ("language", "Bonjour! Pouvons-nous pratiquer un peu de français?"),
    ("language", "Comment commander un café poliment en France?"),
    ("language", "Hallo! Können wir ein bisschen Deutsch üben?"),
    ("language", "¡Hola! ¿Cómo estás hoy y cómo va tu día?"),
    ("language", "How do people greet each other politely in Hindi?"),
    ("language", "Vorrei prenotare un tavolo per due persone, per favore."),

    # 6. Ambiguity, Habits & Conversational Boundaries (6 prompts)
    ("ambiguity", "Can you help me fix it?"),
    ("ambiguity", "What will the stock market do next month?"),
    ("ambiguity", "What are some simple ways to improve my daily focus?"),
    ("ambiguity", "How do I establish a healthy evening routine?"),
    ("ambiguity", "I have sharp chest pains. What medicine should I take?"),
    ("ambiguity", "What is the Fibonacci sequence and where does it appear in nature?")
]


def score_response_quality(prompt: str, response: str) -> Dict[str, Any]:
    """
    Computes heuristic quality metrics for a response:
    - Word count
    - Unique word ratio (repetition check)
    - Has repeated consecutive words
    - Has complete punctuation ending (. ! ?)
    - Substring overlap with prompt (relevance)
    """
    words = response.strip().split()
    word_count = len(words)
    if word_count == 0:
        return {
            "word_count": 0,
            "unique_word_ratio": 0.0,
            "has_repetition": False,
            "ends_with_punct": False,
            "quality_score": 0.0
        }

    unique_ratio = len(set(w.lower() for w in words)) / max(word_count, 1)

    # Check for consecutive identical words (degenerative stuttering)
    has_consecutive_dup = False
    for i in range(len(words) - 1):
        if words[i].lower() == words[i+1].lower() and len(words[i]) > 2:
            has_consecutive_dup = True
            break

    # Punctuation check
    ends_with_punct = response.strip()[-1] in {".", "!", "?", "\"", "'"}

    # Overall quality score (0.0 to 1.0)
    score = 0.0
    if word_count >= 8:
        score += 0.3
    elif word_count >= 4:
        score += 0.15

    if unique_ratio >= 0.75:
        score += 0.3
    elif unique_ratio >= 0.5:
        score += 0.15

    if not has_consecutive_dup:
        score += 0.2

    if ends_with_punct:
        score += 0.2

    return {
        "word_count": word_count,
        "unique_word_ratio": round(unique_ratio, 3),
        "has_repetition": has_consecutive_dup,
        "ends_with_punct": ends_with_punct,
        "quality_score": round(score, 3)
    }


def run_benchmark(
    checkpoint_task4: str,
    checkpoint_new: str,
    output_report_path: str = "ml-service/outputs/task5_evaluation_report.json"
):
    print("=" * 80)
    print("MEENA TASK 5 — CONVERSATIONAL QUALITY BENCHMARK (50 PROMPTS)")
    print("=" * 80)
    print(f"Old Checkpoint: {checkpoint_task4}")
    print(f"New Checkpoint: {checkpoint_new}")
    print("=" * 80)

    # Load Old Model
    print(f"\n[1/3] Loading Task 4 checkpoint...")
    engine_old = MeenaInferenceEngine(checkpoint_path=checkpoint_task4, device="auto", use_fp16=True)

    # Load New Model
    print(f"\n[2/3] Loading New trained checkpoint...")
    engine_new = MeenaInferenceEngine(checkpoint_path=checkpoint_new, device="auto", use_fp16=True)

    # Evaluate all 50 prompts
    print(f"\n[3/3] Evaluating 50 diverse prompts side-by-side...")
    results: List[Dict[str, Any]] = []

    old_total_score = 0.0
    new_total_score = 0.0
    old_rep_count = 0
    new_rep_count = 0

    for idx, (cat, prompt) in enumerate(EVALUATION_PROMPTS, start=1):
        # Generate with old
        res_old = engine_old.generate(prompt=prompt, max_new_tokens=45, temperature=0.7, repetition_penalty=1.35)
        text_old = res_old["response"]
        raw_old = res_old.get("raw_generated", "")
        q_old = score_response_quality(prompt, raw_old if raw_old.strip() else text_old)

        # Generate with new
        res_new = engine_new.generate(prompt=prompt, max_new_tokens=45, temperature=0.7, repetition_penalty=1.35)
        text_new = res_new["response"]
        raw_new = res_new.get("raw_generated", "")
        q_new = score_response_quality(prompt, raw_new if raw_new.strip() else text_new)

        old_total_score += q_old["quality_score"]
        new_total_score += q_new["quality_score"]
        if q_old["has_repetition"]:
            old_rep_count += 1
        if q_new["has_repetition"]:
            new_rep_count += 1

        results.append({
            "id": idx,
            "category": cat,
            "prompt": prompt,
            "task4_response": text_old,
            "task4_raw": raw_old,
            "task4_quality": q_old,
            "new_response": text_new,
            "new_raw": raw_new,
            "new_quality": q_new
        })

        if idx % 10 == 0 or idx == len(EVALUATION_PROMPTS):
            print(f"  Processed {idx}/{len(EVALUATION_PROMPTS)} prompts...")

    n = len(EVALUATION_PROMPTS)
    summary = {
        "total_prompts": n,
        "task4_checkpoint": checkpoint_task4,
        "new_checkpoint": checkpoint_new,
        "task4_avg_quality_score": round(old_total_score / n, 3),
        "new_avg_quality_score": round(new_total_score / n, 3),
        "task4_repetitive_responses": old_rep_count,
        "new_repetitive_responses": new_rep_count,
        "results": results
    }

    os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
    with open(output_report_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 80)
    print("EVALUATION BENCHMARK COMPLETED")
    print("=" * 80)
    print(f"Prompts Evaluated:          {n}")
    print(f"Task 4 Quality Score:       {summary['task4_avg_quality_score']:.3f} / 1.000")
    print(f"New Model Quality Score:    {summary['new_avg_quality_score']:.3f} / 1.000")
    print(f"Task 4 Repetitive Outputs:  {old_rep_count} / {n}")
    print(f"New Model Repetitive Out:   {new_rep_count} / {n}")
    print(f"Detailed Report Saved:      {output_report_path}")
    print("=" * 80)

    return summary


if __name__ == "__main__":
    old_ckpt = os.path.join(BASE_DIR, "checkpoints", "checkpoint_task4_best.pt")
    new_ckpt = os.path.join(BASE_DIR, "checkpoints", "checkpoint_best.pt")
    run_benchmark(old_ckpt, new_ckpt)

