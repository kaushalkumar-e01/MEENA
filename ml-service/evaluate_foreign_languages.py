"""
MEENA — Task 6 Foreign Language Capability Evaluation

Empirically tests French, German, Spanish, and Hindi prompts across:
- Greetings and pleasantries
- Basic vocabulary / phrases
- Language consistency in output
- Reliable vs weak/unsupported language assessment
"""

import os
import sys
import json
import re

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from meena_inference import MeenaInferenceEngine

FOREIGN_TEST_PROMPTS = [
    # French
    {"lang": "French", "prompt": "Bonjour! Comment allez-vous?", "expected": ["bonjour", "bien", "merci"]},
    {"lang": "French", "prompt": "Comment dit-on 'Thank you' en français?", "expected": ["merci", "beaucoup"]},
    {"lang": "French", "prompt": "Je voudrais un café s'il vous plaît.", "expected": ["café", "croissant", "voilà"]},

    # German
    {"lang": "German", "prompt": "Guten Tag! Wie geht es Ihnen?", "expected": ["gut", "danke", "tag"]},
    {"lang": "German", "prompt": "Wie heißt du?", "expected": ["ich", "heiße", "name"]},
    {"lang": "German", "prompt": "Ich lerne Deutsch und trinke gern Kaffee.", "expected": ["deutsch", "gut", "wunderbar"]},

    # Spanish
    {"lang": "Spanish", "prompt": "¡Hola! ¿Cómo estás hoy?", "expected": ["hola", "bien", "gracias"]},
    {"lang": "Spanish", "prompt": "¿Dónde está la biblioteca más cercana?", "expected": ["biblioteca", "cerca", "calle"]},
    {"lang": "Spanish", "prompt": "Me gusta mucho escuchar música latina.", "expected": ["música", "excelente", "canción"]},

    # Hindi
    {"lang": "Hindi", "prompt": "Namaste! Aap kaise hain?", "expected": ["namaste", "theek", "shukriya", "achha"]},
    {"lang": "Hindi", "prompt": "Hindi mein 'water' ko kya kehte hain?", "expected": ["paani", "jal", "kehte"]},
    {"lang": "Hindi", "prompt": "Dhanyavaad aapki madad ke liye.", "expected": ["swagat", "koi", "baat", "nahi"]}
]


def evaluate_languages(checkpoint_path: str):
    print("=" * 70)
    print("MEENA — FOREIGN LANGUAGE EMPIRICAL EVALUATION")
    print(f"Testing Checkpoint: {checkpoint_path}")
    print("=" * 70)

    engine = MeenaInferenceEngine(checkpoint_path=checkpoint_path, device="auto")

    lang_results = {}

    for item in FOREIGN_TEST_PROMPTS:
        lang = item["lang"]
        p = item["prompt"]
        exp = item["expected"]

        res = engine.generate(p, max_new_tokens=30, temperature=0.7)
        raw = res["raw_generated"]
        clean = res["response"]
        fallback = res["is_fallback"]

        # Check if words match expected target language
        matched = [w for w in exp if w.lower() in raw.lower()]

        if lang not in lang_results:
            lang_results[lang] = {
                "total": 0,
                "matches": 0,
                "fallbacks": 0,
                "samples": []
            }

        lang_results[lang]["total"] += 1
        if matched:
            lang_results[lang]["matches"] += 1
        if fallback:
            lang_results[lang]["fallbacks"] += 1

        lang_results[lang]["samples"].append({
            "prompt": p,
            "raw": raw,
            "clean": clean,
            "fallback": fallback,
            "matched_expected": matched
        })

    print("\n" + "=" * 70)
    print("RESULTS BY LANGUAGE:")
    print("=" * 70)
    for lang, data in lang_results.items():
        total = data["total"]
        matches = data["matches"]
        fb = data["fallbacks"]
        print(f"[{lang.upper()}] Total: {total} | Concept Matches: {matches}/{total} | Fallbacks: {fb}/{total}")
        for s in data["samples"]:
            print(f"  Q: {s['prompt']}")
            print(f"  A (Clean): {s['clean']}")
            print(f"  A (Raw):   {s['raw']}")
            print()

    return lang_results


if __name__ == "__main__":
    ckpt = os.path.join(BASE_DIR, "checkpoints", "checkpoint_task5_best.pt")
    evaluate_languages(ckpt)

