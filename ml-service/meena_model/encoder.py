"""
MEENA — Evolved Transformer Encoder

Implements the Evolved Transformer Encoder block discovered by So et al. (ICML 2019):
- Discovered branched lower structure combining Multi-Head Self-Attention in parallel
  with a Gated Linear Unit and Wide Depthwise Separable 1D Convolution.
- Exactly 1 Encoder Block as specified in Adiwardana et al. (Google Brain, 2020).
"""

import torch
import torch.nn as nn
from typing import Optional
from .config import EvolvedTransformerConfig
from .modules import (
    PositionalEncoding,
    GatedLinearUnit,
    DepthwiseSeparableConv1d,
    MultiHeadAttention,
    FeedForward
)


class EvolvedTransformerEncoderLayer(nn.Module):
    """
    A single Evolved Transformer Encoder block (Cell):
    Parallel branching of:
      1. Multi-Head Self-Attention
      2. GLU + Wide Depthwise Separable 1D Convolution (Kernel Size 9)
    Followed by branch summation, residual connection, and Swish Feed-Forward layer.
    """
    def __init__(self, config: EvolvedTransformerConfig):
        super().__init__()
        self.d_model = config.d_model

        # Left Branch: Multi-Head Self-Attention
        self.ln_attn = nn.LayerNorm(config.d_model, eps=config.layer_norm_eps)
        self.self_attn = MultiHeadAttention(
            d_model=config.d_model,
            n_heads=config.n_heads,
            dropout=config.dropout
        )

        # Right Branch: GLU + Wide Depthwise Separable 1D Conv
        self.ln_glu = nn.LayerNorm(config.d_model, eps=config.layer_norm_eps)
        self.glu = GatedLinearUnit(
            d_model=config.d_model,
            activation=config.glu_activation
        )
        self.conv = DepthwiseSeparableConv1d(
            channels=config.d_model,
            kernel_size=config.kernel_size_enc
        )
        self.ln_conv = nn.LayerNorm(config.d_model, eps=config.layer_norm_eps)

        self.branch_dropout = nn.Dropout(config.dropout)

        # Feed-Forward Sublayer
        self.ln_ffn = nn.LayerNorm(config.d_model, eps=config.layer_norm_eps)
        self.ffn = FeedForward(
            d_model=config.d_model,
            d_ff=config.d_ff,
            dropout=config.dropout,
            activation=config.activation
        )
        self.ffn_dropout = nn.Dropout(config.dropout)
        self.final_ln = nn.LayerNorm(config.d_model, eps=config.layer_norm_eps)

    def forward(
        self,
        x: torch.Tensor,
        src_key_padding_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Args:
            x: [batch_size, src_len, d_model]
            src_key_padding_mask: [batch_size, src_len] (True for pad tokens to ignore)
        Returns:
            [batch_size, src_len, d_model]
        """
        # --- Branched Lower Block ---
        # 1. Left Branch: Self-Attention
        x_attn_in = self.ln_attn(x)
        attn_out = self.self_attn(
            query=x_attn_in,
            key=x_attn_in,
            value=x_attn_in,
            key_padding_mask=src_key_padding_mask
        )

        # 2. Right Branch: GLU + Wide Depthwise Conv
        x_glu_in = self.ln_glu(x)
        glu_out = self.glu(x_glu_in)
        conv_out = self.conv(glu_out)
        conv_out = self.ln_conv(conv_out)

        # 3. Sum parallel branches and apply residual connection
        h_mid = x + self.branch_dropout(attn_out + conv_out)

        # --- Feed-Forward Sublayer ---
        h_ffn_in = self.ln_ffn(h_mid)
        ffn_out = self.ffn(h_ffn_in)
        out = h_mid + self.ffn_dropout(ffn_out)

        return self.final_ln(out)


class EvolvedTransformerEncoder(nn.Module):
    """
    The complete Evolved Transformer Encoder stack.
    Contains Token Embeddings, Sinusoidal Positional Encoding, and EXACTLY 1 Encoder Layer.
    """
    def __init__(self, config: EvolvedTransformerConfig, embedding: Optional[nn.Embedding] = None):
        super().__init__()
        self.config = config
        self.d_model = config.d_model

        if embedding is not None:
            self.embedding = embedding
        else:
            self.embedding = nn.Embedding(
                num_embeddings=config.vocab_size,
                embedding_dim=config.d_model,
                padding_idx=config.pad_token_id
            )

        self.embed_scale = config.d_model ** 0.5
        self.pos_encoder = PositionalEncoding(
            d_model=config.d_model,
            max_seq_len=config.max_seq_len,
            dropout=config.dropout
        )

        # Exactly 1 Evolved Transformer Encoder layer per architecture specification
        self.layers = nn.ModuleList([
            EvolvedTransformerEncoderLayer(config)
            for _ in range(config.num_encoder_layers)
        ])
        assert len(self.layers) == 1, "Evolved Transformer Encoder must have exactly 1 layer"

    def forward(
        self,
        src_tokens: torch.Tensor,
        src_key_padding_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Args:
            src_tokens: [batch_size, src_len] LongTensor of token IDs
            src_key_padding_mask: [batch_size, src_len] BoolTensor (True for pad tokens)
        Returns:
            encoder_hidden_states: [batch_size, src_len, d_model]
        """
        # If padding mask is not explicitly provided, derive from pad_token_id
        if src_key_padding_mask is None and self.config.pad_token_id is not None:
            src_key_padding_mask = (src_tokens == self.config.pad_token_id)

        # 1. Embed tokens with scaling and sinusoidal positional encoding
        x = self.embedding(src_tokens) * self.embed_scale
        x = self.pos_encoder(x)

        # 2. Pass through the 1 Evolved Transformer Encoder Layer
        for layer in self.layers:
            x = layer(x, src_key_padding_mask=src_key_padding_mask)

        return x
