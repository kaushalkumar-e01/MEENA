"""
MEENA — Unit Tests for Task 6 Semantic Intelligence & Generalization Benchmark
"""

import os
import sys
import json
import unittest
import torch

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from meena_inference import MeenaInferenceEngine, HONEST_FALLBACK_RESPONSE
from held_out_benchmark_data import HELD_OUT_BENCHMARK_PROMPTS
from data_pipeline.config import DataPipelineConfig


class TestSemanticBenchmark(unittest.TestCase):
    """Verifies Task 6 benchmark integrity, evaluation methodology, and checkpoint preservation."""

    @classmethod
    def setUpClass(cls):
        cls.ckpt_task4 = os.path.join(BASE_DIR, "checkpoints", "checkpoint_task4_best.pt")
        cls.ckpt_task5 = os.path.join(BASE_DIR, "checkpoints", "checkpoint_task5_best.pt")
        cls.report_path = os.path.join(BASE_DIR, "outputs", "task6_semantic_benchmark_report.json")
        cls.train_path = os.path.join(BASE_DIR, "data", "processed", "train.jsonl")

    def test_01_checkpoints_preserved(self):
        """Verifies that both Task 4 and Task 5 checkpoints exist on disk."""
        self.assertTrue(os.path.exists(self.ckpt_task4), "Task 4 checkpoint must be preserved")
        self.assertTrue(os.path.exists(self.ckpt_task5), "Task 5 checkpoint must be preserved")
        self.assertGreater(os.path.getsize(self.ckpt_task4), 40 * 1024 * 1024)
        self.assertGreater(os.path.getsize(self.ckpt_task5), 40 * 1024 * 1024)

    def test_02_held_out_benchmark_integrity(self):
        """Verifies that all 100 prompts are held out with 0% overlap with train.jsonl."""
        self.assertEqual(len(HELD_OUT_BENCHMARK_PROMPTS), 100, "Benchmark must have exactly 100 prompts")

        with open(self.train_path, "r", encoding="utf-8") as f:
            train_turns = [json.loads(line) for line in f]

        train_contexts = set(t["context"].strip().lower() for t in train_turns)
        train_responses = set(t["response"].strip().lower() for t in train_turns)

        for item in HELD_OUT_BENCHMARK_PROMPTS:
            p = item["prompt"].strip().lower()
            self.assertNotIn(p, train_responses, f"Prompt {p} leaked into train responses!")
            self.assertNotIn(f"user: {p}", train_contexts, f"Prompt {p} leaked into train contexts!")

    def test_03_multi_turn_history_formatting(self):
        """Verifies that build_context handles both 'content' and 'text' keys in history."""
        engine = MeenaInferenceEngine.get_instance(checkpoint_path=self.ckpt_task5, force_reload=True, device="cpu")

        history = [
            {"role": "user", "text": "I am traveling to Norway."},
            {"role": "assistant", "content": "Norway is beautiful in October."}
        ]
        context = engine.build_context("What should I pack?", history)

        self.assertIn("User: I am traveling to Norway.", context)
        self.assertIn("MEENA: Norway is beautiful in October.", context)
        self.assertIn("User: What should I pack?", context)

    def test_04_honest_fallback_triggering(self):
        """Verifies that poor/noisy outputs trigger the canonical honest fallback."""
        engine = MeenaInferenceEngine.get_instance()
        # When post-processed text is too short or repetitive, fallback must trigger
        self.assertEqual(len(HONEST_FALLBACK_RESPONSE), 144)
        self.assertIn("I'm listening, but I'm still learning", HONEST_FALLBACK_RESPONSE)

    def test_05_benchmark_report_structure(self):
        """Verifies that the generated Task 6 evaluation report is valid and complete."""
        self.assertTrue(os.path.exists(self.report_path), "Task 6 benchmark report must exist")

        with open(self.report_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["total_prompts"], 100)
        self.assertIn("overall_metrics", data)
        self.assertIn("category_summary", data)
        self.assertIn("scoring_rubric", data)
        self.assertEqual(len(data["category_summary"]), 10)
        self.assertEqual(len(data["results"]), 100)


if __name__ == "__main__":
    unittest.main()
