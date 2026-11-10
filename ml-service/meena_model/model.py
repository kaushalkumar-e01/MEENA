"""
MEENA — Evolved Transformer Sequence-to-Sequence Conversational Model

Assembles the complete neural architecture:
- 1 Evolved Transformer Encoder block
- 13 Evolved Transformer Decoder blocks
- Shared subword embeddings and tied output projection
- Autoregressive conversational decoding (Greedy, Temperature, Top-K, Top-P Nucleus)
- Mixed precision and gradient checkpointing support
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Dict, Any, List

from .config import EvolvedTransformerConfig
from .encoder import EvolvedTransformerEncoder
from .decoder import EvolvedTransformerDecoder


class MeenaEvolvedTransformer(nn.Module):
    """
    The complete MEENA neural conversational model implementing:
    - 1 Evolved Transformer Encoder Layer
    - 13 Evolved Transformer Decoder Layers
    - Shared token embeddings with output projection weight tying
    """
    def __init__(self, config: Optional[EvolvedTransformerConfig] = None):
        super().__init__()
        if config is None:
            config = EvolvedTransformerConfig()
        self.config = config

        # Shared Token Embedding
        self.shared_embedding = nn.Embedding(
            num_embeddings=config.vocab_size,
            embedding_dim=config.d_model,
            padding_idx=config.pad_token_id
        )

        # 1 Encoder Layer
        self.encoder = EvolvedTransformerEncoder(config, embedding=self.shared_embedding)

        # 13 Decoder Layers
        self.decoder = EvolvedTransformerDecoder(config, embedding=self.shared_embedding)

        # Output Vocabulary Projection Head
        self.output_projection = nn.Linear(config.d_model, config.vocab_size, bias=False)

        # Weight Tying (Press & Wolf, 2017)
        if config.tie_word_embeddings:
            self.output_projection.weight = self.shared_embedding.weight

        # Parameter initialization
        self._init_parameters()

    def _init_parameters(self):
        """
        Xavier uniform initialization for linear projections and normal for embeddings.
        """
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
        nn.init.normal_(self.shared_embedding.weight, mean=0.0, std=self.config.d_model ** -0.5)

    def count_parameters(self) -> Dict[str, int]:
        """
        Returns a breakdown of trainable parameters across model components.
        """
        encoder_params = sum(p.numel() for p in self.encoder.layers.parameters() if p.requires_grad)
        decoder_params = sum(p.numel() for p in self.decoder.layers.parameters() if p.requires_grad)
        embed_params = self.shared_embedding.weight.numel()
        total_params = sum(p.numel() for p in self.parameters() if p.requires_grad)

        return {
            "encoder_block_params": encoder_params,
            "decoder_blocks_params": decoder_params,
            "embedding_params": embed_params,
            "total_trainable_params": total_params,
            "encoder_layer_count": len(self.encoder.layers),
            "decoder_layer_count": len(self.decoder.layers),
        }

    def encode(
        self,
        src_tokens: torch.Tensor,
        src_key_padding_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Runs the 1-block Evolved Transformer Encoder.
        """
        return self.encoder(src_tokens, src_key_padding_mask=src_key_padding_mask)

    def decode(
        self,
        tgt_tokens: torch.Tensor,
        memory: torch.Tensor,
        tgt_mask: Optional[torch.Tensor] = None,
        tgt_key_padding_mask: Optional[torch.Tensor] = None,
        memory_key_padding_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Runs the 13-block Evolved Transformer Decoder.
        """
        return self.decoder(
            tgt_tokens=tgt_tokens,
            memory=memory,
            tgt_mask=tgt_mask,
            tgt_key_padding_mask=tgt_key_padding_mask,
            memory_key_padding_mask=memory_key_padding_mask
        )

    def forward(
        self,
        src_tokens: torch.Tensor,
        tgt_tokens: torch.Tensor,
        src_key_padding_mask: Optional[torch.Tensor] = None,
        tgt_key_padding_mask: Optional[torch.Tensor] = None,
        memory_key_padding_mask: Optional[torch.Tensor] = None,
        tgt_mask: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None
    ) -> Dict[str, Any]:
        """
        Standard Seq2Seq forward pass.
        Args:
            src_tokens: [batch_size, src_len]
            tgt_tokens: [batch_size, tgt_len] (typically shifted right target tokens)
            labels: Optional [batch_size, tgt_len] target labels for Cross-Entropy loss computation
        Returns:
            Dict containing:
                "logits": [batch_size, tgt_len, vocab_size]
                "loss": Cross-entropy loss (if labels provided)
                "encoder_memory": [batch_size, src_len, d_model]
        """
        # 1. Encode source tokens
        memory = self.encode(src_tokens, src_key_padding_mask=src_key_padding_mask)

        # Align memory_key_padding_mask with src_key_padding_mask if not explicitly given
        if memory_key_padding_mask is None:
            memory_key_padding_mask = src_key_padding_mask
            if memory_key_padding_mask is None and self.config.pad_token_id is not None:
                memory_key_padding_mask = (src_tokens == self.config.pad_token_id)

        # 2. Decode target tokens through the 13 ET blocks
        decoder_hidden = self.decode(
            tgt_tokens=tgt_tokens,
            memory=memory,
            tgt_mask=tgt_mask,
            tgt_key_padding_mask=tgt_key_padding_mask,
            memory_key_padding_mask=memory_key_padding_mask
        )

        # 3. Project to vocabulary logits
        logits = self.output_projection(decoder_hidden)

        output = {
            "logits": logits,
            "encoder_memory": memory
        }

        # 4. Optional Cross-Entropy Loss computation with label smoothing & ignore index
        if labels is not None:
            loss = F.cross_entropy(
                logits.view(-1, self.config.vocab_size),
                labels.view(-1),
                ignore_index=self.config.pad_token_id,
                label_smoothing=0.1
            )
            output["loss"] = loss

        return output

    @torch.no_grad()
    def generate(
        self,
        src_tokens: torch.Tensor,
        max_new_tokens: int = 64,
        min_new_tokens: int = 3,
        temperature: float = 0.7,
        top_k: int = 40,
        top_p: float = 0.9,
        repetition_penalty: float = 1.35,
        no_repeat_ngram_size: int = 3,
        bos_token_id: Optional[int] = None,
        eos_token_id: Optional[int] = None,
        pad_token_id: Optional[int] = None,
        unk_token_id: Optional[int] = None,
        src_key_padding_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Autoregressive generation supporting Temperature, Top-K, Top-P (Nucleus) sampling,
        Repetition Penalty, N-gram blocking, and min token constraints.
        Args:
            src_tokens: [batch_size, src_len] or [1, src_len]
            max_new_tokens: Maximum number of tokens to generate
            min_new_tokens: Minimum tokens before allowing EOS
            temperature: Sampling temperature (> 0.0)
            top_k: Top-K filtering (0 to disable)
            top_p: Top-P nucleus filtering (1.0 to disable)
            repetition_penalty: Penalty factor (> 1.0) applied to previously generated tokens
            no_repeat_ngram_size: Prevents identical n-grams from repeating
        Returns:
            generated_tokens: [batch_size, generated_seq_len] including BOS
        """
        self.eval()
        device = src_tokens.device
        bsz = src_tokens.size(0)

        bos_id = bos_token_id if bos_token_id is not None else self.config.bos_token_id
        eos_id = eos_token_id if eos_token_id is not None else self.config.eos_token_id
        pad_id = pad_token_id if pad_token_id is not None else self.config.pad_token_id
        unk_id = unk_token_id if unk_token_id is not None else self.config.unk_token_id

        # 1. Encode source prompt once
        memory = self.encode(src_tokens, src_key_padding_mask=src_key_padding_mask)
        memory_mask = src_key_padding_mask
        if memory_mask is None and pad_id is not None:
            memory_mask = (src_tokens == pad_id)

        # 2. Initialize target tokens with BOS
        generated = torch.full((bsz, 1), bos_id, dtype=torch.long, device=device)
        finished = torch.zeros(bsz, dtype=torch.bool, device=device)

        # 3. Autoregressive decoding loop
        for step in range(max_new_tokens):
            # Generate causal mask for current target sequence length
            curr_len = generated.size(1)
            tgt_mask = self.decoder.generate_square_subsequent_mask(curr_len, device=device)

            # Decode through 13 ET blocks
            hidden = self.decode(
                tgt_tokens=generated,
                memory=memory,
                tgt_mask=tgt_mask,
                tgt_key_padding_mask=None,
                memory_key_padding_mask=memory_mask
            )

            # Logits for the latest position only: [batch_size, vocab_size]
            next_token_logits = self.output_projection(hidden[:, -1, :])

            # Suppress pad, bos, and unk from being sampled
            if pad_id is not None:
                next_token_logits[:, pad_id] = -float("Inf")
            if bos_id is not None:
                next_token_logits[:, bos_id] = -float("Inf")
            if unk_id is not None:
                next_token_logits[:, unk_id] = -float("Inf")

            # Min new tokens: suppress EOS before minimum length
            if step < min_new_tokens and eos_id is not None:
                next_token_logits[:, eos_id] = -float("Inf")

            # Apply frequency-aware repetition penalty
            if repetition_penalty > 1.0:
                for i in range(bsz):
                    gen_list = generated[i].tolist()
                    tok_counts = {}
                    for tok_id in gen_list:
                        tok_counts[tok_id] = tok_counts.get(tok_id, 0) + 1
                    for tok_id, count in tok_counts.items():
                        # Compound penalty for tokens that have appeared repeatedly
                        penalty = repetition_penalty ** min(count, 3)
                        if next_token_logits[i, tok_id] > 0:
                            next_token_logits[i, tok_id] /= penalty
                        else:
                            next_token_logits[i, tok_id] *= penalty

            # Apply No-Repeat N-Gram blocking
            if no_repeat_ngram_size > 0 and curr_len >= no_repeat_ngram_size:
                for i in range(bsz):
                    gen_list = generated[i].tolist()
                    ngram_prefix = tuple(gen_list[-(no_repeat_ngram_size - 1):])
                    for j in range(len(gen_list) - no_repeat_ngram_size + 1):
                        if tuple(gen_list[j:j + no_repeat_ngram_size - 1]) == ngram_prefix:
                            forbidden = gen_list[j + no_repeat_ngram_size - 1]
                            next_token_logits[i, forbidden] = -float("Inf")

            # Apply temperature
            if temperature > 0:
                next_token_logits = next_token_logits / max(temperature, 1e-4)

                # Top-K filtering
                if top_k > 0:
                    indices_to_remove = next_token_logits < torch.topk(next_token_logits, top_k)[0][..., -1, None]
                    next_token_logits[indices_to_remove] = -float("Inf")

                # Top-P (Nucleus) filtering
                if 0.0 < top_p < 1.0:
                    sorted_logits, sorted_indices = torch.sort(next_token_logits, descending=True)
                    cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

                    # Remove tokens with cumulative probability above top_p
                    sorted_indices_to_remove = cumulative_probs > top_p
                    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                    sorted_indices_to_remove[..., 0] = 0

                    indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)
                    next_token_logits[indices_to_remove] = -float("Inf")

                probs = F.softmax(next_token_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
            else:
                # Greedy decoding (argmax)
                next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)

            # If a sequence already produced EOS, output PAD
            if finished.any():
                next_token = torch.where(finished.unsqueeze(1), torch.full_like(next_token, pad_id), next_token)

            generated = torch.cat([generated, next_token], dim=1)

            # Check for EOS
            finished = finished | (next_token.squeeze(1) == eos_id)
            if finished.all():
                break

        return generated
