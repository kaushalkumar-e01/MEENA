"""
Unit Test Suite for MEENA Data Pipeline, Tokenizer & PyTorch DataLoaders

Tests all requirements specified in Task 2:
1. Dataset loading and turn extraction.
2. Multi-turn conversation reconstruction.
3. Deduplication and invalid data filtering.
4. Train, validation, and test separation (Zero conversation ID leakage).
5. Tokenizer training, saving, and persistence.
6. Tokenizer loading and text encode/decode roundtrip.
7. Special token IDs (PAD=0, BOS=1, EOS=2, UNK=3).
8. Dynamic padding and boolean attention key padding masks.
9. Decoder input and target label shifting (Teacher Forcing).
10. DataLoader batch shapes and tensor types.
11. Forward-pass smoke test feeding a real DataLoader batch into the Task 1 MeenaEvolvedTransformer.
"""

import sys
import os
import shutil
import tempfile
import unittest
import torch

# Ensure ml-service is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_pipeline.config import DataPipelineConfig
from data_pipeline.tokenizer import MeenaTokenizer
from data_pipeline.dataset_prep import (
    clean_text,
    build_conversation_turns,
    split_conversations,
    prepare_dataset_pipeline,
    generate_expanded_conversational_corpus
)
from data_pipeline.dataset import (
    MeenaConversationalDataset,
    MeenaCollateFn,
    create_dataloader
)
from meena_model.config import EvolvedTransformerConfig
from meena_model.model import MeenaEvolvedTransformer


class TestDataPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp(prefix="meena_test_pipeline_")
        cls.config = DataPipelineConfig(
            base_dir=cls.temp_dir,
            raw_data_dir=os.path.join(cls.temp_dir, "raw"),
            processed_data_dir=os.path.join(cls.temp_dir, "processed"),
            tokenizer_dir=os.path.join(cls.temp_dir, "tokenizer"),
            vocab_size=1000,
            batch_size=2,
            max_seq_len=64,
            max_conversations=50
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_01_clean_text_normalization(self):
        """Test 1: Verify text normalization strips control chars while preserving meaning & contractions."""
        raw = "  Hello \u201cMEENA\u201d!   I\u2019m   feeling happy\x00\x08 today.\n\n\nHow are you?  "
        cleaned = clean_text(raw)
        self.assertEqual(cleaned, 'Hello "MEENA"! I\'m feeling happy today.\nHow are you?')

    def test_02_conversation_reconstruction(self):
        """Test 2: Verify multi-turn conversations are reconstructed into proper (context, response) pairs."""
        convs = [{
            "id": "c1",
            "turns": [
                ("user", "Hello!"),
                ("assistant", "Hi there!"),
                ("user", "What is MEENA?"),
                ("assistant", "MEENA is an AI companion.")
            ]
        }]
        turns = build_conversation_turns(convs, max_history=2)
        self.assertEqual(len(turns), 2)
        # Turn 1
        self.assertEqual(turns[0].context, "User: Hello!")
        self.assertEqual(turns[0].response, "Hi there!")
        # Turn 2
        self.assertIn("User: What is MEENA?", turns[1].context)
        self.assertEqual(turns[1].response, "MEENA is an AI companion.")

    def test_03_deduplication_and_filtering(self):
        """Test 3: Verify duplicate (context, response) turns are deduplicated."""
        convs = [
            {
                "id": "c1",
                "turns": [("user", "Hi"), ("assistant", "Hello!")]
            },
            {
                "id": "c2",
                "turns": [("user", "Hi"), ("assistant", "Hello!")]
            }
        ]
        turns = build_conversation_turns(convs)
        self.assertEqual(len(turns), 1, "Duplicate conversation pair was not filtered")

    def test_04_split_separation_zero_leakage(self):
        """Test 4: Verify train, validation, and test splits have ZERO conversation ID leakage."""
        convs = generate_expanded_conversational_corpus(target_count=60)
        train_convs, val_convs, test_convs = split_conversations(
            convs, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1, seed=42
        )

        train_ids = {c["id"] for c in train_convs}
        val_ids = {c["id"] for c in val_convs}
        test_ids = {c["id"] for c in test_convs}

        self.assertEqual(len(train_ids.intersection(val_ids)), 0, "Train and Validation share conversation IDs!")
        self.assertEqual(len(train_ids.intersection(test_ids)), 0, "Train and Test share conversation IDs!")
        self.assertEqual(len(val_ids.intersection(test_ids)), 0, "Validation and Test share conversation IDs!")
        self.assertEqual(len(train_ids) + len(val_ids) + len(test_ids), len(convs))

    def test_05_tokenizer_train_and_save(self):
        """Test 5: Verify tokenizer training on training split and artifact saving."""
        # Prepare small dataset
        meta = prepare_dataset_pipeline(self.config)
        train_file = meta["split_counts"]["train"]["filepath"]

        def text_iter():
            import json
            with open(train_file, "r", encoding="utf-8") as f:
                for line in f:
                    d = json.loads(line)
                    yield d["context"]
                    yield d["response"]

        tokenizer = MeenaTokenizer.train_from_iterator(text_iter(), self.config)
        self.assertGreater(tokenizer.get_vocab_size(), 10)

        tokenizer.save(self.config.tokenizer_dir)
        self.assertTrue(os.path.exists(os.path.join(self.config.tokenizer_dir, "tokenizer.json")))
        self.assertTrue(os.path.exists(os.path.join(self.config.tokenizer_dir, "tokenizer_config.json")))

    def test_06_tokenizer_loading_and_roundtrip(self):
        """Test 6: Verify loaded tokenizer encodes and decodes text faithfully."""
        tokenizer = MeenaTokenizer.load(self.config.tokenizer_dir, self.config)
        test_phrase = "Good morning MEENA! How are you feeling today?"

        token_ids = tokenizer.encode(test_phrase, add_special_tokens=False)
        self.assertIsInstance(token_ids, list)
        self.assertGreater(len(token_ids), 0)

        decoded = tokenizer.decode(token_ids)
        self.assertEqual(decoded.strip(), test_phrase.strip())

    def test_07_special_token_id_guarantees(self):
        """Test 7: Verify special tokens have exact fixed IDs: PAD=0, BOS=1, EOS=2, UNK=3."""
        tokenizer = MeenaTokenizer.load(self.config.tokenizer_dir, self.config)

        self.assertEqual(tokenizer.pad_token_id, 0)
        self.assertEqual(tokenizer.bos_token_id, 1)
        self.assertEqual(tokenizer.eos_token_id, 2)
        self.assertEqual(tokenizer.unk_token_id, 3)

        self.assertEqual(tokenizer.tokenizer.token_to_id("<pad>"), 0)
        self.assertEqual(tokenizer.tokenizer.token_to_id("<bos>"), 1)
        self.assertEqual(tokenizer.tokenizer.token_to_id("<eos>"), 2)
        self.assertEqual(tokenizer.tokenizer.token_to_id("<unk>"), 3)

    def test_08_dynamic_padding_and_masks(self):
        """Test 8: Verify dynamic batch padding and key padding boolean masks."""
        tokenizer = MeenaTokenizer.load(self.config.tokenizer_dir, self.config)
        collate_fn = MeenaCollateFn(tokenizer=tokenizer, max_seq_len=self.config.max_seq_len)

        raw_batch = [
            {"context_ids": [10, 15, 20], "response_ids": [30, 35]},
            {"context_ids": [10, 15, 20, 25, 30], "response_ids": [40, 45, 50, 55]}
        ]

        batch = collate_fn(raw_batch)

        # src_tokens should be padded to length 5
        self.assertEqual(batch["src_tokens"].shape, (2, 5))
        self.assertEqual(batch["src_tokens"][0, 3].item(), tokenizer.pad_token_id)
        self.assertEqual(batch["src_tokens"][0, 4].item(), tokenizer.pad_token_id)

        # src_key_padding_mask should be True at padded positions
        self.assertTrue(batch["src_key_padding_mask"][0, 3].item())
        self.assertTrue(batch["src_key_padding_mask"][0, 4].item())
        self.assertFalse(batch["src_key_padding_mask"][0, 0].item())

    def test_09_teacher_forcing_target_shifting(self):
        """
        Test 9: Verify strict autoregressive target shifting:
        tgt_tokens starts with <bos>, labels ends with <eos>.
        For every position t, tgt_tokens[:, t+1] == labels[:, t].
        """
        tokenizer = MeenaTokenizer.load(self.config.tokenizer_dir, self.config)
        collate_fn = MeenaCollateFn(tokenizer=tokenizer, max_seq_len=self.config.max_seq_len)

        # Sequence of response IDs
        resp = [101, 102, 103]
        raw_batch = [{"context_ids": [50], "response_ids": resp}]

        batch = collate_fn(raw_batch)
        tgt_tokens = batch["tgt_tokens"][0]
        labels = batch["labels"][0]

        # tgt_tokens: [<bos>, 101, 102, 103]
        # labels:     [101, 102, 103, <eos>]
        self.assertEqual(tgt_tokens[0].item(), tokenizer.bos_token_id)
        self.assertEqual(labels[-1].item(), tokenizer.eos_token_id)

        self.assertEqual(tgt_tokens.tolist(), [tokenizer.bos_token_id, 101, 102, 103])
        self.assertEqual(labels.tolist(), [101, 102, 103, tokenizer.eos_token_id])

        # Verify shift relationship
        for t in range(len(resp)):
            self.assertEqual(tgt_tokens[t + 1].item(), labels[t].item())

    def test_10_dataloader_batches(self):
        """Test 10: Verify DataLoader yields valid PyTorch batches with correct dtypes."""
        tokenizer = MeenaTokenizer.load(self.config.tokenizer_dir, self.config)
        loader = create_dataloader("train", tokenizer, self.config, batch_size=2)

        batch = next(iter(loader))
        self.assertIn("src_tokens", batch)
        self.assertIn("tgt_tokens", batch)
        self.assertIn("labels", batch)
        self.assertIn("src_key_padding_mask", batch)
        self.assertIn("tgt_key_padding_mask", batch)

        self.assertEqual(batch["src_tokens"].dtype, torch.long)
        self.assertEqual(batch["tgt_tokens"].dtype, torch.long)
        self.assertEqual(batch["labels"].dtype, torch.long)
        self.assertEqual(batch["src_key_padding_mask"].dtype, torch.bool)
        self.assertEqual(batch["tgt_key_padding_mask"].dtype, torch.bool)

    def test_11_forward_pass_smoke_test_with_task1_model(self):
        """
        Test 11: End-to-end integration smoke test!
        Feeds a real DataLoader batch directly through the Task 1 MeenaEvolvedTransformer model.
        Verifies forward pass logits and finite scalar cross-entropy loss.
        """
        tokenizer = MeenaTokenizer.load(self.config.tokenizer_dir, self.config)
        loader = create_dataloader("train", tokenizer, self.config, batch_size=2)
        batch = next(iter(loader))

        # Initialize Task 1 Evolved Transformer model with matching vocab size
        vocab_size = tokenizer.get_vocab_size()
        model_config = EvolvedTransformerConfig(
            num_encoder_layers=1,
            num_decoder_layers=13,
            d_model=64,
            n_heads=4,
            d_ff=128,
            max_seq_len=64,
            vocab_size=vocab_size,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            unk_token_id=tokenizer.unk_token_id
        )
        model = MeenaEvolvedTransformer(model_config)
        model.eval()

        with torch.no_grad():
            out = model(
                src_tokens=batch["src_tokens"],
                tgt_tokens=batch["tgt_tokens"],
                src_key_padding_mask=batch["src_key_padding_mask"],
                tgt_key_padding_mask=batch["tgt_key_padding_mask"],
                labels=batch["labels"]
            )

        logits = out["logits"]
        loss = out["loss"]

        # 1. Logits shape: [batch_size, tgt_len, vocab_size]
        expected_shape = (batch["tgt_tokens"].size(0), batch["tgt_tokens"].size(1), vocab_size)
        self.assertEqual(logits.shape, expected_shape)
        self.assertFalse(torch.isnan(logits).any(), "Logits contain NaN values")

        # 2. Loss is a valid positive finite scalar
        self.assertIsNotNone(loss)
        self.assertFalse(torch.isnan(loss).item(), "Loss is NaN")
        self.assertFalse(torch.isinf(loss).item(), "Loss is Inf")
        self.assertGreater(loss.item(), 0.0, "Cross entropy loss must be positive")


if __name__ == "__main__":
    unittest.main()
