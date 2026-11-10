"""
MEENA — Evolved Transformer Submodules

Contains the specialized neural primitives discovered in the Evolved Transformer (So et al., 2019):
1. Gated Linear Units (GLU / SwiGLU)
2. Wide Depthwise Separable 1D Convolutions (bidirectional for Encoder)
3. Causal Wide Depthwise Separable 1D Convolutions (left-padded for Decoder)
4. Scaled Dot-Product Multi-Head Attention (Self & Cross)
5. Sinusoidal Positional Encoding
6. Swish-activated Feed-Forward Networks
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional


class PositionalEncoding(nn.Module):
    """
    Standard sinusoidal positional encoding.
    PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
    """
    def __init__(self, d_model: int, max_seq_len: int = 512, dropout: float = 0.1):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_seq_len, d_model)
        position = torch.arange(0, max_seq_len, dtype=torch.float32).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2, dtype=torch.float32) * (-math.log(10000.0) / d_model)
        )

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)  # [1, max_seq_len, d_model]
        self.register_buffer("pe", pe, persistent=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Tensor of shape [batch_size, seq_len, d_model]
        Returns:
            Tensor of shape [batch_size, seq_len, d_model] with positional encoding added.
        """
        seq_len = x.size(1)
        if seq_len > self.pe.size(1):
            raise ValueError(
                f"Sequence length {seq_len} exceeds max_seq_len {self.pe.size(1)}"
            )
        x = x + self.pe[:, :seq_len, :].to(dtype=x.dtype)
        return self.dropout(x)


class GatedLinearUnit(nn.Module):
    """
    Gated Linear Unit (Dauphin et al., 2017) used in the Evolved Transformer:
    GLU(x) = (x W + b) (*) sigmoid(x V + c)
    Or SwiGLU:
    SwiGLU(x) = (x W + b) (*) swish(x V + c)
    """
    def __init__(self, d_model: int, activation: str = "glu", bias: bool = True):
        super().__init__()
        self.d_model = d_model
        self.activation_type = activation
        # Projects d_model -> 2 * d_model
        self.proj = nn.Linear(d_model, 2 * d_model, bias=bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [batch, seq_len, d_model]
        projected = self.proj(x)
        a, b = projected.chunk(2, dim=-1)
        if self.activation_type == "swiglu":
            return a * F.silu(b)
        # Standard GLU
        return a * torch.sigmoid(b)


class DepthwiseSeparableConv1d(nn.Module):
    """
    Bidirectional Wide Depthwise Separable 1D Convolution for the Evolved Transformer Encoder.
    Applies symmetric padding to maintain sequence length.
    """
    def __init__(self, channels: int, kernel_size: int = 9, bias: bool = True):
        super().__init__()
        assert kernel_size % 2 == 1, "kernel_size must be odd for symmetric padding"
        self.padding = (kernel_size - 1) // 2

        # 1. Depthwise convolution: spatial filtering per channel
        self.depthwise = nn.Conv1d(
            in_channels=channels,
            out_channels=channels,
            kernel_size=kernel_size,
            padding=self.padding,
            groups=channels,
            bias=bias
        )
        # 2. Pointwise convolution: channel mixing (1x1 conv)
        self.pointwise = nn.Conv1d(
            in_channels=channels,
            out_channels=channels,
            kernel_size=1,
            bias=bias
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: [batch_size, seq_len, channels]
        Returns:
            [batch_size, seq_len, channels]
        """
        # Conv1d expects [batch_size, channels, seq_len]
        x_transposed = x.transpose(1, 2)
        out = self.depthwise(x_transposed)
        out = self.pointwise(out)
        return out.transpose(1, 2)


class CausalDepthwiseSeparableConv1d(nn.Module):
    """
    Causal Wide Depthwise Separable 1D Convolution for the Evolved Transformer Decoder.
    Strictly left-pads inputs by (kernel_size - 1) and 0 on the right, ensuring that
    output token at position t depends ONLY on input tokens at positions <= t.
    Zero future information leakage.
    """
    def __init__(self, channels: int, kernel_size: int = 11, bias: bool = True):
        super().__init__()
        self.kernel_size = kernel_size
        self.left_padding = kernel_size - 1

        self.depthwise = nn.Conv1d(
            in_channels=channels,
            out_channels=channels,
            kernel_size=kernel_size,
            padding=0,  # Explicit manual causal padding in forward()
            groups=channels,
            bias=bias
        )
        self.pointwise = nn.Conv1d(
            in_channels=channels,
            out_channels=channels,
            kernel_size=1,
            bias=bias
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: [batch_size, seq_len, channels]
        Returns:
            [batch_size, seq_len, channels] with strict causal receptive field.
        """
        # Transpose to [batch, channels, seq_len]
        x_transposed = x.transpose(1, 2)
        # Pad left by (kernel_size - 1), right by 0
        x_padded = F.pad(x_transposed, (self.left_padding, 0))
        out = self.depthwise(x_padded)
        out = self.pointwise(out)
        return out.transpose(1, 2)


class MultiHeadAttention(nn.Module):
    """
    Standard scaled dot-product multi-head attention supporting:
    - 2D/3D causal attention masks (additive or boolean)
    - 2D key padding masks [batch_size, src_len]
    """
    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.1, bias: bool = True):
        super().__init__()
        assert d_model % n_heads == 0, "d_model must be divisible by n_heads"

        self.d_model = d_model
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
        self.scale = 1.0 / math.sqrt(self.head_dim)

        self.q_proj = nn.Linear(d_model, d_model, bias=bias)
        self.k_proj = nn.Linear(d_model, d_model, bias=bias)
        self.v_proj = nn.Linear(d_model, d_model, bias=bias)
        self.out_proj = nn.Linear(d_model, d_model, bias=bias)

        self.dropout = nn.Dropout(p=dropout)

    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        attn_mask: Optional[torch.Tensor] = None,
        key_padding_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Args:
            query: [batch_size, tgt_len, d_model]
            key:   [batch_size, src_len, d_model]
            value: [batch_size, src_len, d_model]
            attn_mask: [tgt_len, src_len] or [batch_size, n_heads, tgt_len, src_len]
                       Boolean True or large negative float indicates masked position.
            key_padding_mask: [batch_size, src_len]
                              Boolean True indicates token to IGNORE (padding).
        Returns:
            [batch_size, tgt_len, d_model]
        """
        bsz, tgt_len, _ = query.size()
        src_len = key.size(1)

        # 1. Project and reshape to [batch, n_heads, seq_len, head_dim]
        q = self.q_proj(query).view(bsz, tgt_len, self.n_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(key).view(bsz, src_len, self.n_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(value).view(bsz, src_len, self.n_heads, self.head_dim).transpose(1, 2)

        # 2. Scaled Dot-Product Attention Scores
        # scores: [batch, n_heads, tgt_len, src_len]
        scores = torch.matmul(q, k.transpose(-2, -1)) * self.scale

        # 3. Apply Attention Mask (e.g. causal upper-triangular mask)
        fill_val = -1e4 if scores.dtype == torch.float16 else -1e9
        if attn_mask is not None:
            if attn_mask.dtype == torch.bool:
                scores = scores.masked_fill(attn_mask, fill_val)
            else:
                scores = scores + attn_mask

        # 4. Apply Key Padding Mask (ignore padding tokens)
        if key_padding_mask is not None:
            # key_padding_mask: [batch, src_len] -> [batch, 1, 1, src_len]
            mask_expanded = key_padding_mask.unsqueeze(1).unsqueeze(2)
            scores = scores.masked_fill(mask_expanded, fill_val)

        # 5. Softmax & Dropout
        attn_weights = F.softmax(scores, dim=-1)
        # Avoid NaN if an entire row was masked (e.g. all padding)
        attn_weights = torch.nan_to_num(attn_weights, nan=0.0)
        attn_weights = self.dropout(attn_weights)

        # 6. Weighted Sum and Output Projection
        # [batch, n_heads, tgt_len, head_dim] -> [batch, tgt_len, d_model]
        context = torch.matmul(attn_weights, v)
        context = context.transpose(1, 2).contiguous().view(bsz, tgt_len, self.d_model)
        return self.out_proj(context)


class FeedForward(nn.Module):
    """
    Position-wise Feed-Forward Network using Swish (SiLU) activation:
    FFN(x) = Swish(x W_1 + b_1) W_2 + b_2
    """
    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1, activation: str = "swish"):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(p=dropout)

        if activation == "relu":
            self.act = nn.ReLU()
        elif activation == "gelu":
            self.act = nn.GELU()
        else:
            self.act = nn.SiLU()  # Swish

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear2(self.dropout(self.act(self.linear1(x))))
