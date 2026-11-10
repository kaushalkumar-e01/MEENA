"""
MEENA — Unit Tests for Dataset Quality, Split Integrity & Zero-Leakage (Task 5)
"""

import os
import sys
import json
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from data_pipeline.config import DataPipelineConfig
from meena_inference import MeenaInferenceEngine


class TestDatasetQuality(unittest.TestCase):
    """Verifies that the dataset satisfies all Task 5 data quality constraints."""

    @classmethod
    def setUpClass(cls):
        cls.config = DataPipelineConfig()
        cls.train_path = os.path.join(cls.config.processed_data_dir, "train.jsonl")
        cls.val_path = os.path.join(cls.config.processed_data_dir, "val.jsonl")
        cls.test_path = os.path.join(cls.config.processed_data_dir, "test.jsonl")

    def _load_turns(self, path: str):
        self.assertTrue(os.path.exists(path), f"File {path} must exist")
        turns = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    turns.append(json.loads(line))
        return turns

    def test_splits_exist_and_non_empty(self):
        train = self._load_turns(self.train_path)
        val = self._load_turns(self.val_path)
        test = self._load_turns(self.test_path)

        self.assertGreaterEqual(len(train), 50, "Train split should have substantial turns")
        self.assertGreaterEqual(len(val), 10, "Val split should have at least 10 turns")
        self.assertGreaterEqual(len(test), 10, "Test split should have at least 10 turns")

    def test_zero_synthetic_tags(self):
        """Ensures absolutely no cheap (Context update #...) loop tags exist in any split."""
        for path in [self.train_path, self.val_path, self.test_path]:
            turns = self._load_turns(path)
            for turn in turns:
                self.assertNotIn("(Context update #", turn.get("context", ""), f"Synthetic tag found in {path}")
                self.assertNotIn("(Context update #", turn.get("response", ""), f"Synthetic tag found in {path}")

    def test_all_target_responses_unique(self):
        """Ensures every response within each split is unique."""
        for path in [self.train_path, self.val_path, self.test_path]:
            turns = self._load_turns(path)
            responses = [t["response"].strip() for t in turns]
            self.assertEqual(len(responses), len(set(responses)), f"Found duplicate responses in {path}")

    def test_zero_cross_split_target_leakage(self):
        """Ensures 0% target response leakage between train and val/test splits."""
        train = self._load_turns(self.train_path)
        val = self._load_turns(self.val_path)
        test = self._load_turns(self.test_path)

        train_resps = set(t["response"].strip() for t in train)
        val_resps = set(t["response"].strip() for t in val)
        test_resps = set(t["response"].strip() for t in test)

        val_leakage = val_resps.intersection(train_resps)
        test_leakage = test_resps.intersection(train_resps)

        self.assertEqual(len(val_leakage), 0, f"Target leakage between train and val: {val_leakage}")
        self.assertEqual(len(test_leakage), 0, f"Target leakage between train and test: {test_leakage}")

    def test_checkpoint_best_loads_and_generates(self):
        """Ensures checkpoint_best.pt loads and generates non-empty text."""
        ckpt_path = os.path.join(BASE_DIR, "checkpoints", "checkpoint_best.pt")
        self.assertTrue(os.path.exists(ckpt_path), "checkpoint_best.pt must exist")

        engine = MeenaInferenceEngine(checkpoint_path=ckpt_path, device="cpu", use_fp16=False)
        result = engine.generate("Hello MEENA, how are you?")
        self.assertIn("response", result)
        self.assertGreater(len(result["response"]), 0)


if __name__ == "__main__":
    unittest.main()

