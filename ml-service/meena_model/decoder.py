"""
MEENA — Evolved Transformer Decoder

Implements the Evolved Transformer Decoder block discovered by So et al. (ICML 2019):
- Branched lower section incorporating Masked Multi-Head Self-Attention in parallel
  with a Causal Wide Depthwise Separable 1D Convolution (Kernel Size 11).
- Multi-Head Cross-Attention to Encoder representations.
- Position-wise Swish Feed-Forward Network.
- Exactly 13 Decoder Blocks as specified in Adiwardana et al. (Google Brain, 2020).
"""

import torch
import torch.nn as nn
import torch.utils.checkpoint
from typing import Optional
from .config import EvolvedTransformerConfig
from .modules import (
    PositionalEncoding,
    CausalDepthwiseSeparableConv1d,
    MultiHeadAttention,
    FeedForward
)


class EvolvedTransformerDecoderLayer(nn.Module):
    """
    A single Evolved Transformer Decoder block (Cell):
    1. Parallel Lower Branch:
       - Masked Causal Multi-Head Self-Attention
       - Causal Wide Depthwise Separable 1D Convolution (Kernel Size 11, left-padded)
    2. Multi-Head Cross-Attention (Encoder-Decoder)
    3. Position-wise Swish Feed-Forward Network
    """
    def __init__(self, config: EvolvedTransformerConfig):
        super().__init__()
        self.d_model = config.d_model

        # 1. Parallel Lower Branches:
        # 1a. Causal Self-Attention
        self.ln_self_attn = nn.LayerNorm(config.d_model, eps=config.layer_norm_eps)
        self.self_attn = MultiHeadAttention(
            d_model=config.d_model,
            n_heads=config.n_heads,
            dropout=config.dropout
        )

        # 1b. Causal Wide Depthwise Separable Convolution
        self.ln_conv = nn.LayerNorm(config.d_model, eps=config.layer_norm_eps)
        self.causal_conv = CausalDepthwiseSeparableConv1d(
            channels=config.d_model,
            kernel_size=config.kernel_size_dec
        )
        self.conv_act = nn.SiLU()  # Swish
        self.ln_conv_out = nn.LayerNorm(config.d_model, eps=config.layer_norm_eps)

        self.branch_dropout = nn.Dropout(config.dropout)

        # 2. Encoder-Decoder Cross-Attention
        self.ln_cross_attn = nn.LayerNorm(config.d_model, eps=config.layer_norm_eps)
        self.cross_attn = MultiHeadAttention(
            d_model=config.d_model,
            n_heads=config.n_heads,
            dropout=config.dropout
        )
        self.cross_dropout = nn.Dropout(config.dropout)

        # 3. Feed-Forward Sublayer
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
        y: torch.Tensor,
        memory: torch.Tensor,
        tgt_mask: Optional[torch.Tensor] = None,
        tgt_key_padding_mask: Optional[torch.Tensor] = None,
        memory_key_padding_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Args:
            y: [batch_size, tgt_len, d_model] target sequence representations
            memory: [batch_size, src_len, d_model] encoder hidden state representations
            tgt_mask: [tgt_len, tgt_len] causal upper-triangular mask
            tgt_key_padding_mask: [batch_size, tgt_len] (True for target pad tokens)
            memory_key_padding_mask: [batch_size, src_len] (True for encoder pad tokens)
        Returns:
            [batch_size, tgt_len, d_model]
        """
        # --- 1. Branched Lower Section ---
        # 1a. Causal Self-Attention
        y_self_in = self.ln_self_attn(y)
        self_attn_out = self.self_attn(
            query=y_self_in,
            key=y_self_in,
            value=y_self_in,
            attn_mask=tgt_mask,
            key_padding_mask=tgt_key_padding_mask
        )

        # 1b. Causal Depthwise Conv
        y_conv_in = self.ln_conv(y)
        conv_out = self.causal_conv(y_conv_in)
        conv_out = self.conv_act(conv_out)
        conv_out = self.ln_conv_out(conv_out)

        # Combine parallel branches with residual
        y_mid1 = y + self.branch_dropout(self_attn_out + conv_out)

        # --- 2. Encoder-Decoder Cross-Attention ---
        y_cross_in = self.ln_cross_attn(y_mid1)
        cross_out = self.cross_attn(
            query=y_cross_in,
            key=memory,
            value=memory,
            key_padding_mask=memory_key_padding_mask
        )
        y_mid2 = y_mid1 + self.cross_dropout(cross_out)

        # --- 3. Feed-Forward Sublayer ---
        y_ffn_in = self.ln_ffn(y_mid2)
        ffn_out = self.ffn(y_ffn_in)
        out = y_mid2 + self.ffn_dropout(ffn_out)

        return self.final_ln(out)


class EvolvedTransformerDecoder(nn.Module):
    """
    The complete Evolved Transformer Decoder stack.
    Contains Token Embeddings, Sinusoidal Positional Encoding, and EXACTLY 13 Decoder Layers.
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

        # Exactly 13 Evolved Transformer Decoder layers per architecture specification
        self.layers = nn.ModuleList([
            EvolvedTransformerDecoderLayer(config)
            for _ in range(config.num_decoder_layers)
        ])
        assert len(self.layers) == 13, "Evolved Transformer Decoder must have exactly 13 layers"

    @staticmethod
    def generate_square_subsequent_mask(sz: int, device: Optional[torch.device] = None) -> torch.Tensor:
        """
        Generates an upper-triangular boolean causal mask:
        Positions where mask == True are forbidden (masked out).
        """
        mask = torch.triu(torch.ones(sz, sz, device=device, dtype=torch.bool), diagonal=1)
        return mask

    def forward(
        self,
        tgt_tokens: torch.Tensor,
        memory: torch.Tensor,
        tgt_mask: Optional[torch.Tensor] = None,
        tgt_key_padding_mask: Optional[torch.Tensor] = None,
        memory_key_padding_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Args:
            tgt_tokens: [batch_size, tgt_len] LongTensor of target token IDs
            memory: [batch_size, src_len, d_model] encoder hidden representations
            tgt_mask: [tgt_len, tgt_len] causal mask (auto-generated if None)
            tgt_key_padding_mask: [batch_size, tgt_len] BoolTensor (True for pad tokens)
            memory_key_padding_mask: [batch_size, src_len] BoolTensor (True for pad tokens)
        Returns:
            [batch_size, tgt_len, d_model]
        """
        bsz, tgt_len = tgt_tokens.size()

        # Generate causal mask if not passed
        if tgt_mask is None:
            tgt_mask = self.generate_square_subsequent_mask(tgt_len, device=tgt_tokens.device)

        if tgt_key_padding_mask is None and self.config.pad_token_id is not None:
            tgt_key_padding_mask = (tgt_tokens == self.config.pad_token_id)

        # 1. Embed target tokens with scaling and positional encoding
        y = self.embedding(tgt_tokens) * self.embed_scale
        y = self.pos_encoder(y)

        # 2. Pass sequentially through the 13 Evolved Transformer Decoder Layers
        for layer in self.layers:
            if self.config.use_gradient_checkpointing and self.training:
                # Custom forward wrapper for gradient checkpointing
                def create_custom_forward(module):
                    def custom_forward(*inputs):
                        return module(*inputs)
                    return custom_forward

                y = torch.utils.checkpoint.checkpoint(
                    create_custom_forward(layer),
                    y,
                    memory,
                    tgt_mask,
                    tgt_key_padding_mask,
                    memory_key_padding_mask,
                    use_reentrant=False
                )
            else:
                y = layer(
                    y,
                    memory=memory,
                    tgt_mask=tgt_mask,
                    tgt_key_padding_mask=tgt_key_padding_mask,
                    memory_key_padding_mask=memory_key_padding_mask
                )

        return y
