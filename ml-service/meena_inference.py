"""
MEENA — Neural Model Inference Engine

Loads and serves the trained 1-Encoder + 13-Decoder Evolved Transformer:
- Singleton lifecycle to eliminate redundant model reloading
- Automatic GPU (CUDA/FP16) / CPU (FP32) hardware detection and safe fallback
- Conversation context formatting with multi-turn history
- Advanced autoregressive decoding: Repetition penalty, N-gram blocking,
  special token suppression, and min token constraints
- Clean subword detokenization & punctuation post-processing
- Honest fallback when generation does not meet confidence threshold
"""

import os
import re
import sys
import threading
from typing import Dict, List, Optional, Any, Tuple

import torch

# Ensure ml-service root is in sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from meena_model.config import EvolvedTransformerConfig
from meena_model.model import MeenaEvolvedTransformer
from data_pipeline.config import DataPipelineConfig
from data_pipeline.tokenizer import MeenaTokenizer


# Honest fallback response when model output is too brief or noisy
HONEST_FALLBACK_RESPONSE = (
    "I'm listening, but I'm still learning how to phrase my thoughts on that topic. "
    "Could you tell me more about what you mean or ask in another way?"
)


class MeenaInferenceEngine:
    """
    Thread-safe, cached inference engine for the trained MEENA Evolved Transformer.
    """
    _instance: Optional["MeenaInferenceEngine"] = None
    _lock = threading.Lock()

    def __init__(
        self,
        checkpoint_path: Optional[str] = None,
        tokenizer_dir: Optional[str] = None,
        device: str = "auto",
        use_fp16: bool = True
    ):
        self.base_dir = BASE_DIR
        self.checkpoint_path = checkpoint_path or self._resolve_checkpoint_path()
        self.tokenizer_dir = tokenizer_dir or os.path.join(self.base_dir, "data", "tokenizer")
        self.requested_device = device
        self.use_fp16 = use_fp16

        # Hardware Setup
        self.device, self.is_half = self._setup_device()

        # Load Tokenizer
        self.tokenizer = self._load_tokenizer()

        # Load Model
        self.model, self.checkpoint_meta = self._load_model()

    @classmethod
    def get_instance(
        cls,
        checkpoint_path: Optional[str] = None,
        force_reload: bool = False,
        device: str = "auto"
    ) -> "MeenaInferenceEngine":
        """
        Retrieves or initializes the cached singleton inference engine.
        """
        with cls._lock:
            if cls._instance is None or force_reload:
                cls._instance = cls(checkpoint_path=checkpoint_path, device=device)
            return cls._instance

    def _resolve_checkpoint_path(self) -> str:
        """Finds the best available trained checkpoint."""
        ckpt_dir = os.path.join(self.base_dir, "checkpoints")
        candidates = [
            os.path.join(ckpt_dir, "checkpoint_best.pt"),
            os.path.join(ckpt_dir, "checkpoint_latest.pt"),
            os.path.join(ckpt_dir, "checkpoint_epoch_03.pt"),
            os.path.join(ckpt_dir, "checkpoint_epoch_02.pt"),
            os.path.join(ckpt_dir, "checkpoint_epoch_01.pt"),
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        raise FileNotFoundError(
            f"No trained MEENA checkpoints found in {ckpt_dir}. Please run run_training.py first."
        )

    def _setup_device(self) -> Tuple[torch.device, bool]:
        """Detects compute device and floating point precision."""
        if self.requested_device == "cpu":
            return torch.device("cpu"), False

        if torch.cuda.is_available():
            dev = torch.device("cuda:0")
            is_half = self.use_fp16
            return dev, is_half

        return torch.device("cpu"), False

    def _load_tokenizer(self) -> MeenaTokenizer:
        """Loads the exact ByteLevel BPE tokenizer used during training."""
        if not os.path.exists(self.tokenizer_dir):
            raise FileNotFoundError(f"Tokenizer directory not found at {self.tokenizer_dir}")
        data_cfg = DataPipelineConfig(base_dir=self.base_dir)
        tokenizer = MeenaTokenizer.load(self.tokenizer_dir, data_cfg)
        return tokenizer

    def _load_model(self) -> Tuple[MeenaEvolvedTransformer, Dict[str, Any]]:
        """Restores the 1-Encoder + 13-Decoder neural architecture and trained weights."""
        if not os.path.exists(self.checkpoint_path):
            raise FileNotFoundError(f"Checkpoint file not found: {self.checkpoint_path}")

        checkpoint = torch.load(self.checkpoint_path, map_location=self.device, weights_only=False)

        # Restore architecture config
        if "model_config" in checkpoint:
            model_config = EvolvedTransformerConfig.from_dict(checkpoint["model_config"])
        else:
            model_config = EvolvedTransformerConfig(
                num_encoder_layers=1,
                num_decoder_layers=13,
                vocab_size=self.tokenizer.get_vocab_size()
            )

        # Strict validation
        if model_config.num_encoder_layers != 1 or model_config.num_decoder_layers != 13:
            raise ValueError(
                f"Invalid architecture in checkpoint: {model_config.num_encoder_layers} enc / "
                f"{model_config.num_decoder_layers} dec (Expected 1 enc / 13 dec)"
            )

        model = MeenaEvolvedTransformer(model_config)
        model.load_state_dict(checkpoint["model_state_dict"])
        model.to(self.device)

        if self.is_half and self.device.type == "cuda":
            model.half()

        model.eval()

        meta = {
            "epoch": checkpoint.get("epoch", 0),
            "val_loss": checkpoint.get("val_loss", 0.0),
            "val_perplexity": checkpoint.get("val_perplexity", 0.0),
            "architecture": "1_encoder_13_decoder_evolved_transformer",
            "checkpoint_path": self.checkpoint_path
        }
        return model, meta

    def build_context(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        max_turns: int = 4
    ) -> str:
        """
        Formats multi-turn conversation history into model context matching training format:
        User: <text>
        MEENA: <text>
        User: <current message>
        """
        turns: List[str] = []

        if history:
            # Use the most recent N turns
            recent_history = history[-max_turns:]
            for item in recent_history:
                speaker = "User" if item.get("role") in ("user", "human") else "MEENA"
                content = (item.get("content") or item.get("text") or "").strip()
                if content:
                    turns.append(f"{speaker}: {content}")

        # Always append current user prompt
        turns.append(f"User: {prompt.strip()}")
        return "\n".join(turns)

    @torch.no_grad()
    def generate(
        self,
        prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        max_new_tokens: int = 45,
        temperature: float = 0.65,
        top_k: int = 40,
        top_p: float = 0.9,
        repetition_penalty: float = 1.35,
        no_repeat_ngram_size: int = 3,
        min_new_tokens: int = 4
    ) -> Dict[str, Any]:
        """
        Executes neural autoregressive response generation with full anti-repetition guards.
        """
        self.model.eval()

        # 1. Format Context & Tokenize
        context = self.build_context(prompt, history)
        context_ids = self.tokenizer.encode(context, add_special_tokens=False)

        # Truncate context to model max sequence length
        max_ctx_len = self.model.config.max_seq_len
        if len(context_ids) > max_ctx_len:
            context_ids = context_ids[-max_ctx_len:]

        src_tensor = torch.tensor([context_ids], dtype=torch.long, device=self.device)

        # 2. Autoregressive Generation
        token_tensor = self.model.generate(
            src_tokens=src_tensor,
            max_new_tokens=max_new_tokens,
            min_new_tokens=min_new_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            no_repeat_ngram_size=no_repeat_ngram_size,
            bos_token_id=self.tokenizer.bos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id,
            unk_token_id=self.tokenizer.unk_token_id,
        )

        # 3. Decode & Detokenize
        token_list = token_tensor[0].tolist()
        # Drop BOS if present
        if token_list and token_list[0] == self.tokenizer.bos_token_id:
            token_list = token_list[1:]
        # Truncate at EOS if present
        if self.tokenizer.eos_token_id in token_list:
            eos_idx = token_list.index(self.tokenizer.eos_token_id)
            token_list = token_list[:eos_idx]

        raw_text = self.tokenizer.decode(token_list, skip_special_tokens=True)

        # 4. Post-Process & Clean Detokenization
        clean_text = self._post_process(raw_text)

        # 5. Honest Fallback Check
        # Check if output contains sufficient distinct words and non-degenerate structure
        words = re.findall(r"[A-Za-zÀ-ÿ]{2,}", clean_text)
        unique_words = set(w.lower() for w in words)

        # Check for degenerate consecutive word repetition (e.g. "the the")
        tokens = clean_text.split()
        has_consecutive_dup = any(
            tokens[i].lower() == tokens[i+1].lower() and len(tokens[i]) > 1
            for i in range(len(tokens) - 1)
        )

        is_fallback = False
        if len(words) < 4 or len(unique_words) < 3 or has_consecutive_dup:
            clean_text = HONEST_FALLBACK_RESPONSE
            is_fallback = True

        vram_mb = None
        if self.device.type == "cuda":
            vram_mb = round(torch.cuda.memory_allocated(0) / (1024 ** 2), 2)

        return {
            "response": clean_text,
            "raw_generated": raw_text,
            "tokens_generated": len(token_list),
            "is_fallback": is_fallback,
            "model": "MEENA Evolved Transformer (1 Enc + 13 Dec)",
            "device": str(self.device),
            "vram_mb": vram_mb,
            "checkpoint": os.path.basename(self.checkpoint_path)
        }

    @staticmethod
    def _post_process(text: str) -> str:
        """
        Cleans generated text: trims noise, normalizes spacing and punctuation.
        """
        if not text:
            return ""

        # Remove artificial speaker labels if generated
        text = re.sub(r'^(MEENA|User|Assistant):\s*', '', text, flags=re.IGNORECASE)

        # Remove multiple consecutive punctuation
        text = re.sub(r'([,\.\?\!])\s*\1+', r'\1', text)

        # Fix spacing before punctuation (e.g. 'word ,' -> 'word,')
        text = re.sub(r'\s+([,\.\?\!;:])', r'\1', text)

        # Collapse excess whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        # Capitalize first letter
        if text and text[0].islower():
            text = text[0].upper() + text[1:]

        return text

    def get_status(self) -> Dict[str, Any]:
        """Returns runtime diagnostic metrics for API health monitoring."""
        params = self.model.count_parameters()
        vram_mb = None
        if self.device.type == "cuda":
            vram_mb = round(torch.cuda.memory_allocated(0) / (1024 ** 2), 2)

        return {
            "status": "ready",
            "model_architecture": "1_encoder_13_decoder_evolved_transformer",
            "encoder_blocks": params["encoder_layer_count"],
            "decoder_blocks": params["decoder_layer_count"],
            "total_parameters": params["total_trainable_params"],
            "device": str(self.device),
            "fp16_enabled": self.is_half,
            "vram_allocated_mb": vram_mb,
            "checkpoint": os.path.basename(self.checkpoint_path),
            "checkpoint_epoch": self.checkpoint_meta.get("epoch"),
            "val_perplexity": self.checkpoint_meta.get("val_perplexity"),
            "vocab_size": self.tokenizer.get_vocab_size()
        }

