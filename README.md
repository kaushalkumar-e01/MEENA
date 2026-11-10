# MEENA

MEENA (Mindful, Empathetic & Expressive Natural Assistant) is a conversational assistant project with a Next.js chat application, API routes, a standalone machine-learning service, and a PyTorch Evolved Transformer model implementation. The repository contains application and research code; it does not currently include a trained neural checkpoint.

## Intended architecture

The neural model is configured as an encoder-decoder Evolved Transformer with exactly **1 encoder block and 13 decoder blocks**. The implementation includes shared token embeddings, attention and convolution components, and autoregressive decoding. This describes the code's intended/configured architecture, not a claim that a production model has been trained or deployed.

## Features in the codebase

- Chat interface and Next.js API routes for chat, authentication, sharing, checkout, and local ML analysis.
- Optional Gemini API integration for streamed chat responses; a local Antigravity CLI bridge is also attempted before a deterministic fallback response engine.
- Standalone FastAPI service with sentiment and intent classification, TF-IDF knowledge retrieval, topic clustering, and metrics endpoints.
- PyTorch Evolved Transformer model, BPE tokenizer wrapper, conversation data preparation, and model/data-pipeline tests.
- Supabase client integration points and local demo authentication/payment flows.

These are code paths and UI capabilities. External integrations and production behavior require configuration and have not been verified here.

## Technology

- Frontend and web API: Next.js 15, React 19 release candidate, TypeScript, Tailwind CSS, Zustand.
- Web integrations: Google GenAI SDK and Supabase JavaScript client; Razorpay-facing demo checkout UI/API.
- ML service/model: Python, FastAPI, scikit-learn, NumPy, PyTorch, Hugging Face `tokenizers`.
- JavaScript package manager: pnpm (lockfile and workspace file are present).

## Repository layout

```text
src/                         Next.js application, components, state, and API routes
ml-service/main.py           FastAPI ML API (runs small classic ML models at startup)
ml-service/meena_model/      PyTorch Evolved Transformer implementation
ml-service/data_pipeline/    Dataset preparation, tokenizer, and loader code
ml-service/run_data_pipeline.py
ml-service/tests/             Python unit tests
package.json                  Frontend scripts and dependencies
pnpm-lock.yaml                Locked JavaScript dependency graph
Gemini.md                     Project design/implementation notes
brandGuidelines.md            Brand guidelines
```

There is also a `MEENA/` directory containing a nested copy of some root-level project files and generated build/dependency directories. The root-level app and `src/` tree are used by the root `package.json`; the nested copy is not used by these instructions.

## Setup

Requirements: Node.js compatible with the declared Next.js version, pnpm, and (for the ML service) Python 3.10 or newer. Python dependencies are imported by the code, but no Python requirements/lock file is currently included, so the Python environment is not reproducible from this repository alone.

1. Install frontend dependencies from the repository root:

   ```bash
   pnpm install --frozen-lockfile
   ```

2. Copy `.env.example` to `.env.local` and fill only the integrations you intend to use. Keep real credentials out of Git. `GEMINI_API_KEY` enables Gemini chat; `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` configure the Supabase client. The service-role and Razorpay secret variables are examples for server-side integrations and must never be exposed to browser code. `ML_SERVICE_URL` defaults to `http://localhost:8000`; `NEXT_PUBLIC_RAZORPAY_KEY_ID` is a public client key and currently has a demo test placeholder.

3. Start the frontend:

   ```bash
   pnpm dev
   ```

   Open `http://localhost:3000`. `pnpm build` and `pnpm start` are also declared. The declared `lint` script runs `next lint`; check compatibility with the installed Next.js version if you use it.

### ML service

From the repository root, create and activate a Python virtual environment, install the required packages (at minimum FastAPI, Uvicorn, NumPy, and scikit-learn), then run:

```bash
python -m uvicorn main:app --app-dir ml-service --host 127.0.0.1 --port 8000
```

The service exposes `/health`, `/ml/classify-sentiment`, `/ml/classify-intent`, `/ml/similar-contexts`, `/ml/cluster-topics`, and `/ml/model-metrics`. Its current web API routes do not call `ML_SERVICE_URL`; the frontend has a separate TypeScript ML engine/API route.

### Dataset and tokenizer pipeline

From the repository root, install the additional pipeline dependencies (`torch` and `tokenizers`; the model/tests also rely on PyTorch) and run:

```bash
python ml-service/run_data_pipeline.py
```

The script writes train/validation/test JSONL splits, tokenizer artifacts, and metadata under `ml-service/data/`. If raw data files are placed under `ml-service/data/raw/`, the pipeline can consume those; otherwise it builds a synthetic corpus from repeated curated seed conversations. Although current metadata labels the corpus `oasst1_curated` and names OASST1, the preparation code does not download OASST1. The generated JSONL splits and tokenizer model file are excluded by `.gitignore`; the small tokenizer configuration remains trackable. Regenerate generated artifacts with the command above. Inspect and verify dataset provenance and licensing before distributing any externally sourced data.

The tokenizer config records a vocabulary size of 3,101 and special token IDs PAD=0, BOS=1, EOS=2, UNK=3. No trained model checkpoint or model-training script is present in the root project.

## Development status and limitations

This is an in-progress prototype. Authentication now requires configured Supabase credentials; without them, the auth API is disabled. Checkout still stores orders in memory with placeholder payment verification and must not be used for production payments. Gemini requires a valid API key; the alternative local bridge depends on a machine-specific Antigravity executable, with a deterministic response engine fallback. The standalone FastAPI service trains small classifiers in memory at startup from hard-coded examples; reported fit metrics are not held-out evaluation. The PyTorch architecture and tests exist, but no trained checkpoint, training loop, Python dependency manifest, or production deployment configuration is included.

## Before publishing

- Review whether the generated JSONL dataset and tokenizer should be regenerated locally or stored outside Git. They are ignored by default; use Git LFS or external artifact storage if versioned distribution is needed.
- Review `Gemini.md`, `brandGuidelines.md`, and the nested `MEENA/` copy for content and duplication before publishing.
- Configure real credentials only in local environment files or deployment secret storage.
