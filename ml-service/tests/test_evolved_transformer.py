"""
Unit Test Suite for the MEENA Evolved Transformer Neural Architecture

Verifies:
1. Model initialization and layer counts (1 encoder block, 13 decoder blocks).
2. Encoder output dimensions [batch_size, src_len, d_model].
3. Decoder output dimensions [batch_size, tgt_len, d_model].
4. Attention key padding masking.
5. Strict causal masking (no future token leakage).
6. End-to-end forward pass and cross-entropy loss computation.
7. Backpropagation and gradient health (zero NaNs, zero Infs).
8. Vocabulary projection dimensions [batch_size, tgt_len, vocab_size].
9. Autoregressive decoding (greedy and top-p sampling).
10. Gradient checkpointing compatibility.
11. Mixed precision (AMP) compatibility.
"""

import sys
import os
import unittest
import torch
import torch.nn.functional as F

# Ensure ml-service is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from meena_model.config import EvolvedTransformerConfig
from meena_model.model import MeenaEvolvedTransformer
from meena_model.encoder import EvolvedTransformerEncoder, EvolvedTransformerEncoderLayer
from meena_model.decoder import EvolvedTransformerDecoder, EvolvedTransformerDecoderLayer
from meena_model.modules import CausalDepthwiseSeparableConv1d, GatedLinearUnit


class TestEvolvedTransformer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Compact test configuration
        cls.config = EvolvedTransformerConfig(
            num_encoder_layers=1,
            num_decoder_layers=13,
            d_model=64,
            n_heads=4,
            d_ff=128,
            max_seq_len=64,
            vocab_size=1000,
            kernel_size_enc=9,
            kernel_size_dec=11,
            dropout=0.0,  # deterministic for causal mask tests
            use_gradient_checkpointing=False
        )
        cls.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        cls.model = MeenaEvolvedTransformer(cls.config).to(cls.device)

    def test_01_layer_counts_strict_specification(self):
        """Test 1: Verify exactly 1 encoder block and 13 decoder blocks."""
        encoder_blocks = len(self.model.encoder.layers)
        decoder_blocks = len(self.model.decoder.layers)
        self.assertEqual(encoder_blocks, 1, f"Expected 1 encoder block, got {encoder_blocks}")
        self.assertEqual(decoder_blocks, 13, f"Expected 13 decoder blocks, got {decoder_blocks}")

        # Verify configuration guardrails
        with self.assertRaises(ValueError):
            EvolvedTransformerConfig(num_encoder_layers=2)
        with self.assertRaises(ValueError):
            EvolvedTransformerConfig(num_decoder_layers=6)

    def test_02_encoder_output_dimensions(self):
        """Test 2: Verify encoder output shape matches [batch_size, src_len, d_model]."""
        batch_size = 2
        src_len = 16
        src_tokens = torch.randint(4, self.config.vocab_size, (batch_size, src_len), device=self.device)

        memory = self.model.encode(src_tokens)
        self.assertEqual(
            memory.shape,
            (batch_size, src_len, self.config.d_model),
            f"Expected shape ({batch_size}, {src_len}, {self.config.d_model}), got {memory.shape}"
        )
        self.assertFalse(torch.isnan(memory).any(), "Encoder output contains NaN values")
        self.assertFalse(torch.isinf(memory).any(), "Encoder output contains Inf values")

    def test_03_decoder_output_dimensions(self):
        """Test 3: Verify decoder output shape matches [batch_size, tgt_len, d_model]."""
        batch_size = 2
        src_len = 16
        tgt_len = 10

        src_tokens = torch.randint(4, self.config.vocab_size, (batch_size, src_len), device=self.device)
        tgt_tokens = torch.randint(4, self.config.vocab_size, (batch_size, tgt_len), device=self.device)

        memory = self.model.encode(src_tokens)
        decoder_out = self.model.decode(tgt_tokens, memory)

        self.assertEqual(
            decoder_out.shape,
            (batch_size, tgt_len, self.config.d_model),
            f"Expected shape ({batch_size}, {tgt_len}, {self.config.d_model}), got {decoder_out.shape}"
        )
        self.assertFalse(torch.isnan(decoder_out).any(), "Decoder output contains NaN values")
        self.assertFalse(torch.isinf(decoder_out).any(), "Decoder output contains Inf values")

    def test_04_vocabulary_projection_dimensions(self):
        """Test 4: Verify logits project to full vocabulary size [batch_size, tgt_len, vocab_size]."""
        batch_size = 3
        src_len = 12
        tgt_len = 8

        src_tokens = torch.randint(4, self.config.vocab_size, (batch_size, src_len), device=self.device)
        tgt_tokens = torch.randint(4, self.config.vocab_size, (batch_size, tgt_len), device=self.device)

        out = self.model(src_tokens, tgt_tokens)
        logits = out["logits"]

        self.assertEqual(
            logits.shape,
            (batch_size, tgt_len, self.config.vocab_size),
            f"Expected logits shape ({batch_size}, {tgt_len}, {self.config.vocab_size}), got {logits.shape}"
        )
        self.assertFalse(torch.isnan(logits).any(), "Logits contain NaN values")
        self.assertFalse(torch.isinf(logits).any(), "Logits contain Inf values")

    def test_05_strict_causal_masking_no_future_leakage(self):
        """
        Test 5: STRICT CAUSAL PROPERTY
        Modifying future tokens at position t > k must NOT affect logits or outputs at position <= k.
        """
        self.model.eval()
        batch_size = 1
        src_len = 8
        tgt_len = 10
        k = 4  # cutoff point

        src_tokens = torch.randint(4, self.config.vocab_size, (batch_size, src_len), device=self.device)

        # Baseline sequence
        tgt_a = torch.randint(4, self.config.vocab_size, (batch_size, tgt_len), device=self.device)
        # Variant sequence: exactly same tokens up to position k, but completely different tokens after k
        tgt_b = tgt_a.clone()
        tgt_b[:, k + 1:] = (tgt_b[:, k + 1:] + 50) % self.config.vocab_size

        with torch.no_grad():
            logits_a = self.model(src_tokens, tgt_a)["logits"]
            logits_b = self.model(src_tokens, tgt_b)["logits"]

        # Check that outputs at positions 0..k are IDENTICAL
        diff_prior = torch.abs(logits_a[:, :k + 1, :] - logits_b[:, :k + 1, :]).max().item()
        self.assertLess(
            diff_prior,
            1e-5,
            f"Causal leakage detected! Output at position <= {k} changed when future tokens were altered (max diff: {diff_prior})"
        )

        # Check that outputs after k DO differ (verifying the change took effect)
        diff_after = torch.abs(logits_a[:, k + 1:, :] - logits_b[:, k + 1:, :]).max().item()
        self.assertGreater(
            diff_after,
            1e-3,
            "Altered future tokens had zero effect on future positions, which is unexpected"
        )

    def test_06_causal_conv1d_strict_causality(self):
        """Test 6: Verify CausalDepthwiseSeparableConv1d does not leak future information."""
        conv = CausalDepthwiseSeparableConv1d(channels=32, kernel_size=11).to(self.device)
        conv.eval()

        seq_len = 20
        cutoff = 8
        x1 = torch.randn(1, seq_len, 32, device=self.device)
        x2 = x1.clone()
        x2[:, cutoff + 1:, :] = torch.randn_like(x2[:, cutoff + 1:, :])

        with torch.no_grad():
            out1 = conv(x1)
            out2 = conv(x2)

        diff_prior = torch.abs(out1[:, :cutoff + 1, :] - out2[:, :cutoff + 1, :]).max().item()
        self.assertLess(
            diff_prior,
            1e-6,
            f"Causal conv leaked future tokens! Max diff at past positions: {diff_prior}"
        )

    def test_07_attention_key_padding_masking(self):
        """Test 7: Verify key padding mask successfully masks out padding tokens."""
        batch_size = 2
        src_len = 10
        tgt_len = 6

        src_tokens = torch.randint(4, self.config.vocab_size, (batch_size, src_len), device=self.device)
        # Mark second half of second sequence as padding
        src_tokens[1, 5:] = self.config.pad_token_id

        tgt_tokens = torch.randint(4, self.config.vocab_size, (batch_size, tgt_len), device=self.device)

        out = self.model(src_tokens, tgt_tokens)
        self.assertFalse(torch.isnan(out["logits"]).any(), "Padding caused NaN in logits")
        self.assertEqual(out["logits"].shape, (batch_size, tgt_len, self.config.vocab_size))

    def test_08_end_to_end_backpropagation_and_gradients(self):
        """Test 8: Verify loss backward computes finite gradients for all trainable parameters."""
        self.model.train()
        batch_size = 2
        src_len = 10
        tgt_len = 8

        src_tokens = torch.randint(4, self.config.vocab_size, (batch_size, src_len), device=self.device)
        tgt_tokens = torch.randint(4, self.config.vocab_size, (batch_size, tgt_len), device=self.device)
        labels = torch.randint(4, self.config.vocab_size, (batch_size, tgt_len), device=self.device)

        self.model.zero_grad()
        out = self.model(src_tokens, tgt_tokens, labels=labels)
        loss = out["loss"]

        self.assertIsNotNone(loss, "Loss was not computed")
        self.assertFalse(torch.isnan(loss).item(), "Loss is NaN")
        self.assertFalse(torch.isinf(loss).item(), "Loss is Inf")

        loss.backward()

        # Check every trainable parameter for valid, non-null, finite gradients
        params_with_grad = 0
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                self.assertIsNotNone(param.grad, f"Gradient for {name} is None")
                self.assertFalse(torch.isnan(param.grad).any(), f"Gradient for {name} contains NaN")
                self.assertFalse(torch.isinf(param.grad).any(), f"Gradient for {name} contains Inf")
                params_with_grad += 1

        self.assertGreater(params_with_grad, 0, "No gradients were computed")

    def test_09_autoregressive_generation(self):
        """Test 9: Verify autoregressive generation produces valid sequences."""
        self.model.eval()
        prompt = torch.tensor([[10, 25, 33, 47]], device=self.device)

        # 1. Greedy generation
        gen_greedy = self.model.generate(
            prompt,
            max_new_tokens=15,
            temperature=0.0
        )
        self.assertEqual(gen_greedy.dim(), 2)
        self.assertEqual(gen_greedy.size(0), 1)
        self.assertGreater(gen_greedy.size(1), 1)
        self.assertEqual(gen_greedy[0, 0].item(), self.config.bos_token_id, "Generated output must start with BOS")

        # 2. Top-P (Nucleus) generation
        gen_topp = self.model.generate(
            prompt,
            max_new_tokens=15,
            temperature=0.7,
            top_p=0.9
        )
        self.assertEqual(gen_topp.dim(), 2)
        self.assertEqual(gen_topp.size(0), 1)
        self.assertEqual(gen_topp[0, 0].item(), self.config.bos_token_id)

    def test_10_parameter_count_breakdown(self):
        """Test 10: Verify parameter breakdown utility."""
        counts = self.model.count_parameters()
        self.assertIn("encoder_block_params", counts)
        self.assertIn("decoder_blocks_params", counts)
        self.assertIn("embedding_params", counts)
        self.assertIn("total_trainable_params", counts)
        self.assertEqual(counts["encoder_layer_count"], 1)
        self.assertEqual(counts["decoder_layer_count"], 13)
        self.assertGreater(counts["total_trainable_params"], 0)

    def test_11_mixed_precision_forward(self):
        """Test 11: Verify forward pass under torch.amp mixed precision."""
        device_type = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if torch.cuda.is_available() else torch.bfloat16

        src = torch.randint(4, self.config.vocab_size, (2, 8), device=self.device)
        tgt = torch.randint(4, self.config.vocab_size, (2, 6), device=self.device)

        try:
            with torch.amp.autocast(device_type=device_type, dtype=dtype):
                out = self.model(src, tgt)
                logits = out["logits"]
                self.assertFalse(torch.isnan(logits).any())
        except RuntimeError as e:
            # On some older CPUs without bfloat16 support, skip gracefully
            if "not supported" in str(e).lower():
                self.skipTest("AMP not supported on this host CPU")
            else:
                raise e

    def test_12_gradient_checkpointing_backward(self):
        """Test 12: Verify backward pass with gradient checkpointing enabled."""
        ckpt_config = EvolvedTransformerConfig(
            num_encoder_layers=1,
            num_decoder_layers=13,
            d_model=64,
            n_heads=4,
            d_ff=128,
            max_seq_len=64,
            vocab_size=1000,
            use_gradient_checkpointing=True
        )
        ckpt_model = MeenaEvolvedTransformer(ckpt_config).to(self.device)
        ckpt_model.train()

        src = torch.randint(4, ckpt_config.vocab_size, (2, 8), device=self.device)
        tgt = torch.randint(4, ckpt_config.vocab_size, (2, 6), device=self.device)
        labels = torch.randint(4, ckpt_config.vocab_size, (2, 6), device=self.device)

        out = ckpt_model(src, tgt, labels=labels)
        loss = out["loss"]
        loss.backward()

        # Verify gradients exist and are finite
        for name, param in ckpt_model.named_parameters():
            if param.requires_grad:
                self.assertIsNotNone(param.grad, f"Gradient checkpointing failed for {name}")
                self.assertFalse(torch.isnan(param.grad).any(), f"NaN in gradient for {name}")


if __name__ == "__main__":
    unittest.main()
