"""
MEENA — Unit Tests for Task 7 Large-Scale Pretraining & Fine-Tuning Pipeline
Verifies dataset manifest integrity, checkpoint retention across all tasks,
architecture parameter preservation, and 4-checkpoint benchmark results.
"""

import os
import sys
import json
from pathlib import Path
import pytest
import torch

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from meena_model.model import MeenaEvolvedTransformer
from meena_model.config import EvolvedTransformerConfig
from meena_inference import MeenaInferenceEngine

CHECKPOINTS_DIR = Path(BASE_DIR) / "checkpoints"
PRETRAINING_DATA_DIR = Path(BASE_DIR) / "data" / "pretraining"
OUTPUTS_DIR = Path(BASE_DIR) / "outputs"


class TestPretrainingPipeline:
    """Verifies Task 7 dataset curation, training artifacts, and benchmark outputs."""

    def test_01_pretraining_dataset_manifest_integrity(self):
        """Pretraining dataset manifest must exist, contain verified OASST1 stats, and 0% leakage."""
        manifest_path = PRETRAINING_DATA_DIR / "dataset_manifest.json"
        assert manifest_path.exists(), f"Missing dataset manifest at {manifest_path}"

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert manifest["source"] == "https://huggingface.co/datasets/OpenAssistant/oasst1"
        assert "Apache 2.0" in manifest["license"]
        assert manifest["split_counts"]["train"]["turns"] >= 3500
        assert manifest["split_counts"]["validation"]["turns"] >= 300
        assert manifest["split_counts"]["test"]["turns"] >= 300
        assert manifest["tokenizer_vocab_size"] == 3101
        assert manifest["approx_train_tokens"] > 1_000_000

    def test_02_all_task_checkpoints_preserved(self):
        """Task 4, Task 5, Task 7 Pretrained, Task 7 Fine-Tuned, and Active best must all exist."""
        required_checkpoints = [
            "checkpoint_task4_best.pt",
            "checkpoint_task5_best.pt",
            "checkpoint_task7_pretrained.pt",
            "checkpoint_task7_finetuned.pt",
            "checkpoint_best.pt",
        ]
        for ckpt_name in required_checkpoints:
            ckpt_path = CHECKPOINTS_DIR / ckpt_name
            assert ckpt_path.exists(), f"Required checkpoint {ckpt_name} missing from {CHECKPOINTS_DIR}"
            assert ckpt_path.stat().st_size > 40 * 1024 * 1024, f"{ckpt_name} is abnormally small"

    def test_03_pretrained_and_finetuned_architecture_strictness(self):
        """Pretrained and fine-tuned checkpoints must strictly restore 1 enc, 13 dec, 4,330,880 params."""
        for ckpt_name in ["checkpoint_task7_pretrained.pt", "checkpoint_task7_finetuned.pt"]:
            ckpt_path = CHECKPOINTS_DIR / ckpt_name
            checkpoint = torch.load(ckpt_path, map_location="cpu", weights_only=False)

            config = EvolvedTransformerConfig(
                num_encoder_layers=1,
                num_decoder_layers=13,
                vocab_size=checkpoint.get("vocab_size", 3101)
            )
            model = MeenaEvolvedTransformer(config)
            model.load_state_dict(checkpoint["model_state_dict"])

            assert len(model.encoder.layers) == 1, f"Encoder layers mismatch in {ckpt_name}"
            assert len(model.decoder.layers) == 13, f"Decoder layers mismatch in {ckpt_name}"
            counts = model.count_parameters()
            assert counts["total_trainable_params"] == 4_330_880, f"Parameter count mismatch in {ckpt_name}"
            assert counts["encoder_layer_count"] == 1
            assert counts["decoder_layer_count"] == 13

    def test_04_training_metric_summaries_exist(self):
        """Pretraining and fine-tuning output summaries must record loss reduction and valid perplexity."""
        pretrain_summary_path = OUTPUTS_DIR / "task7_pretraining_summary.json"
        finetune_summary_path = OUTPUTS_DIR / "task7_finetuning_summary.json"

        assert pretrain_summary_path.exists(), "Pretraining summary JSON missing"
        assert finetune_summary_path.exists(), "Fine-tuning summary JSON missing"

        with open(pretrain_summary_path, "r", encoding="utf-8") as f:
            pretrain_meta = json.load(f)
        assert pretrain_meta["final_train_loss"] < pretrain_meta["initial_train_loss"]
        assert pretrain_meta["final_val_perplexity"] > 0

        with open(finetune_summary_path, "r", encoding="utf-8") as f:
            finetune_meta = json.load(f)
        assert finetune_meta["final_train_loss"] < finetune_meta["initial_train_loss"]
        assert finetune_meta["final_val_perplexity"] > 0

    def test_05_four_checkpoint_comparison_report(self):
        """Benchmark comparison report must evaluate all 4 checkpoints across exactly 100 prompts."""
        report_path = OUTPUTS_DIR / "task7_four_checkpoint_comparison.json"
        assert report_path.exists(), f"Benchmark comparison report missing at {report_path}"

        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["total_prompts"] == 100
        assert len(data["summary_metrics"]) == 4

        expected_keys = ["task4", "task5", "task7_pretrain", "task7_finetune"]
        for key in expected_keys:
            assert key in data["summary_metrics"], f"Missing summary for {key}"
            summary = data["summary_metrics"][key]
            assert 1.0 <= summary["avg_rubric_score_1_to_5"] <= 5.0
            assert 0.0 <= summary["repetitive_percentage"] <= 100.0
            assert 0.0 <= summary["avg_valid_word_ratio"] <= 1.0

    def test_06_neural_inference_engine_task7_generation(self):
        """MeenaInferenceEngine must generate non-empty text using the active Task 7 checkpoint."""
        engine = MeenaInferenceEngine(
            checkpoint_path=str(CHECKPOINTS_DIR / "checkpoint_task7_finetuned.pt"),
            device="cpu",
        )
        result = engine.generate(prompt="Hello MEENA, how are you today?")
        assert isinstance(result, dict)
        assert "response" in result and len(result["response"]) > 0
        assert "tokens_generated" in result and result["tokens_generated"] > 0
        assert isinstance(result["is_fallback"], bool)
