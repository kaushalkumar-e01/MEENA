# MEENA — Master Project Specification & Engineering Directive

> **CRITICAL DIRECTIVE FOR ALL AI AGENTS & ENGINEERS:**
> Before proposing, designing, or implementing any code, configuration, or architectural modification in the MEENA repository, you **MUST** thoroughly read and adhere to this document and [`brandGuidelines.md`](./brandGuidelines.md). Do not deviate from the architectural principles, design guidelines, tech stack choices, or coding standards specified herein without explicit instruction from the project owner.

---

## 1. Project Overview & Philosophy

### 1.1 What is MEENA?

**MEENA** (Mindful, Empathetic & Expressive Natural Assistant) is a full-stack, emotionally intelligent AI companion and conversational platform. MEENA is designed to move beyond the cold, sterile, robotic transactionality of conventional chatbots and deliver a warm, thoughtful, human-centered conversational experience grounded in active listening, contextual understanding, and memory persistence.

MEENA is also a research-informed project. The original MEENA research paper (Adiwardana et al., Google Brain, 2020) described an open-domain chatbot using an Evolved Transformer architecture with one encoder block and thirteen decoder blocks, trained to minimize perplexity on conversational data. **This application does not reproduce or claim to have trained that architecture.** We use the Google Gemini API as the production language model. The Evolved Transformer reference is preserved for academic context and as an inspiration for MEENA's conversational quality goals.

### 1.2 Core Pillars

1. **Empathy & Active Listening** — MEENA frames responses with warmth, attentiveness, and tact, validating user emotions before diving into problem-solving.
2. **Minimal & Thoughtful Design** — The interface reflects calm, clarity, and breathability, purposefully avoiding generic AI tropes like neon gradients, futuristic holograms, and intrusive spinners.
3. **Continuous Context & Memory** — MEENA recalls relevant past interactions across sessions to offer personalized and meaningful companionship.
4. **Speed & Smoothness** — Real-time streaming token-by-token responses. Target: Time to First Token (TTFT) under 800ms on median connections. Instant optimistic UI updates and frictionless interactions.
5. **Absolute Privacy & Data Sovereignty** — Transparent memory controls, clear data retention policies, one-click history clearing, and full data export.

### 1.3 Evolved Transformer Architecture — Research Context

> **Honesty Notice:** The following describes the academic architecture that inspired MEENA's name and conversational quality targets. It is **not** implemented in this codebase. MEENA uses the Google Gemini API for all language generation.

The original MEENA (Adiwardana et al., 2020) used:
- An Evolved Transformer (ET) sequence-to-sequence model.
- 1 ET encoder block + 13 ET decoder blocks.
- 2.6 billion parameters trained on 341 GB of public social media conversations.
- Evaluation metric: Sensibleness and Specificity Average (SSA).
- Perplexity of 10.2 on the test set.

Our production application achieves comparable conversational quality by integrating the Gemini API, while independently implementing classical ML algorithms for intent classification, semantic retrieval, and topic analysis as described in Section 8.

---

## 2. Technology Stack & Architecture

### 2.1 Stack Overview

| Tier | Technology | Purpose & Rationale |
| :--- | :--- | :--- |
| **Framework** | **Next.js 15 (App Router)** | Full-stack React framework with RSC, Server Actions, and Edge/Node API routes. |
| **Language** | **TypeScript 5+ (Strict Mode)** | End-to-end type safety, reliable refactoring, and structured data schemas. |
| **Styling** | **Tailwind CSS v4 + CSS Variables** | Atomic styling mapped to custom semantic pastel tokens defined in `brandGuidelines.md`. |
| **UI Primitives** | **Radix UI** | Accessible, unstyled, keyboard-navigable UI components (Dialogs, Dropdowns, Tooltips, Select). |
| **Icons** | **Lucide React** | Clean, minimalist, consistent line iconography (1.5px stroke width). |
| **State Management** | **Zustand** | Lightweight, boilerplate-free client state for chat sessions, settings, and UI toggles. |
| **Database** | **PostgreSQL via Supabase** | Relational data persistence with built-in Row Level Security, Storage, and Realtime. |
| **ORM / Querying** | **Prisma ORM** | Type-safe schema migrations, relation modeling, and database queries. |
| **Vector Search** | **pgvector (via Supabase)** | Vector embeddings storage and similarity search for long-term semantic memory retrieval. |
| **Authentication** | **Supabase Auth** | Full-featured auth supporting OAuth (Google, Apple), Email/Password, OTP, Magic Link, Phone OTP, and WebAuthn Passkeys. |
| **AI / LLM Engine** | **Google Gemini API (`@google/genai`)** | `gemini-2.0-flash` for fast chat; `gemini-2.5-pro` for complex reasoning and deep analysis. |
| **Embeddings** | **Gemini Embeddings API** | `gemini-embedding-exp-03-07` (3072 dimensions) for semantic memory retrieval. |
| **Streaming Protocol** | **Server-Sent Events (SSE)** | Real-time token streaming with backpressure control and interruptible responses. |
| **ML Runtime** | **Python (FastAPI microservice)** | Hosts independently trained TF-IDF, SVM, KNN, and K-Means ML models. |
| **File Storage** | **Supabase Storage** | Secure per-user file buckets with RLS policies for uploaded images and documents. |
| **Search** | **Supabase Full-Text Search + pgvector** | Full-text chat search and semantic library search over user documents. |
| **Testing** | **Vitest, React Testing Library, Playwright** | Fast unit/integration tests and reliable end-to-end user journey validation. |
| **Package Manager** | **pnpm** | Fast, disk-efficient package management. |

### 2.2 System Architecture Diagram

```
+------------------------------------------------------------------------+
|                            Client (Browser)                            |
|  Next.js 15 App Router — RSC + Client Components                       |
|  Zustand: chatStore, uiStore, settingsStore, authStore                 |
|  Markdown + KaTeX + Shiki Syntax Highlighter                           |
|  SSE Streaming Receiver — Auto-scroll + Pause + Stop Controls          |
+------------------------+---------------------------+-------------------+
                         |                           |
                   HTTPS / SSE                   HTTPS / REST
                         |                           |
+------------------------v-----------+   +-----------v-------------------+
|       Next.js API Layer            |   |   Python FastAPI ML Service   |
|                                    |   |                               |
|  Middleware:                       |   |  POST /ml/classify-intent     |
|   - Supabase Auth Session Guard    |   |  POST /ml/classify-sentiment  |
|   - Token Bucket Rate Limiter      |   |  POST /ml/similar-contexts    |
|   - CSRF Protection                |   |  GET  /ml/cluster-topics      |
|                                    |   |  GET  /ml/model-metrics       |
|  API Routes:                       |   |                               |
|   - /api/chat          (SSE)       |   |  Models:                      |
|   - /api/conversations (CRUD)      |   |  - TF-IDF + Logistic Reg.    |
|   - /api/messages      (CRUD)      |   |  - TF-IDF + Linear SVM       |
|   - /api/memory        (RAG)       |   |  - TF-IDF + Cosine Sim.      |
|   - /api/attachments   (upload)    |   |  - K-Nearest Neighbors        |
|   - /api/share         (links)     |   |  - K-Means Clustering         |
|   - /api/user          (profile)   |   |  - Sentence Embeddings (MiniLM)|
|   - /api/usage         (quota)     |   +-------------------------------+
+------------------+-----------------+
                   |
        Supabase Client (service role — server only)
                   |
+------------------v-------------------------------------------------+
|                    Supabase / PostgreSQL + pgvector                 |
|                                                                     |
|  Users & Auth Accounts         Conversations & Messages             |
|  Attachments & Storage         Long-Term Memory Embeddings          |
|  User Preferences              Shared Conversation Links            |
|  Usage Records                 ML Feedback Records                  |
|  Device Sessions               Passkey Credentials                  |
+---------------------------------------------------------------------+
                   |
        Google Gemini API (server-side only — key never exposed)
                   |
+------------------v-------------------------------------------------+
|  gemini-2.0-flash      — Default conversational engine              |
|  gemini-2.5-pro        — Deep reasoning, long documents, code       |
|  gemini-embedding-exp-03-07 — Semantic memory embeddings (3072-dim) |
+---------------------------------------------------------------------+
```

---

## 3. Planned Features & Functionality

### 3.1 Core Conversational Experience
- **Live Streaming Chat** — Responses stream token by token with a soft rose-tinted blinking cursor indicator.
- **Rich Message Formatting** — Full Markdown support: headings, tables, blockquotes, ordered/unordered lists, KaTeX mathematical equations, and Shiki-powered syntax-highlighted code blocks with one-click copy.
- **Message Actions** — Copy, Share, Read Aloud, Regenerate, Thumbs Up, Thumbs Down below every assistant message. Edit and Copy above every user message.
- **Message Branching** — Navigate between alternate regenerated responses for any given turn using prev/next branch arrows.
- **Response Pause / Stop** — Immediate AbortController cancellation of streaming generation; button switches between Send and Stop states.
- **Keyboard Shortcuts** — `Enter` to send, `Shift+Enter` for newline, `Ctrl/Cmd+K` to open search, `Ctrl/Cmd+B` to toggle sidebar.

### 3.2 Left Sidebar Navigation
- **MEENA Logo & Name** at top.
- **Sidebar Toggle** — Three-line icon, smooth collapse to icon rail (64px) or full drawer on mobile.
- **New Chat** button.
- **Search Chats** — Full-text and semantic search across conversation titles and message content.
- **Pinned Section** — Pinned conversations stay above recents.
- **Recent Chats** — Chronologically grouped: Today, Yesterday, Previous 7 Days, Older.
- **Auto-Title Generation** — Backend generates a 3–5 word title from the first user message using Gemini.
- **Conversation Context Menu (⋮)** — Share, Rename, Pin/Unpin, Archive, Delete (with confirmation modal).
- **Archived Section** — View and restore archived conversations.
- **Bottom Bar** — User avatar, name, Account menu (My Profile, Settings, Add Account, Switch Account, Upgrade Plan, Log Out).

### 3.3 Main Chat Header
- **Conversation Title** (editable inline).
- **Share Button** — Opens share modal with unique public link generation, link revocation, and conversation preview.
- **Temporary Chat Button** — Incognito icon; visually distinct mode indicator when active.

### 3.4 Temporary / Incognito Chat
- Activated from the main header or a keyboard shortcut.
- Conversations in temporary mode are **never written to `conversations` or `messages` tables**.
- Server maintains an ephemeral in-memory session object for context window purposes only; this is cleared at session end.
- Long-term memory extraction is disabled for temporary sessions.
- Share links cannot be generated from temporary chats.
- A clear persistent banner indicates Temporary Chat is active.
- Users can exit temporary mode and return to their regular chat history at any time.

### 3.5 Message Composer
- Auto-growing textarea with `min-height: 52px`, `max-height: 200px` before scrolling.
- Placeholder: *"Message MEENA..."*
- **Attachment (+) Button** — Expandable menu: Upload Image, Upload File, Take Photo (camera), Attach Multiple Files.
- Supported formats: PDF, TXT, DOCX, CSV, PNG, JPG, JPEG, WebP, GIF, MP4 (future), and plain-text source code files.
- **Attachment Preview Strip** — Thumbnail cards above the input showing filename, size, and × remove button.
- **Microphone Button** — Voice-to-text using the browser Web Speech API; live transcription, recording timer, stop control, permission error handling.
- **Send / Stop Button** — Rose-colored upward arrow; switches to a square stop icon during generation.

### 3.6 Voice Interactions
- **Speech-to-Text (STT)** — Browser Web Speech API (primary), with graceful fallback messaging for unsupported browsers.
- Multilingual transcription where the Speech Recognition API permits.
- Live transcription preview in the composer textarea during recording.
- Recording state indicator (pulsing rose dot + timer).
- **Text-to-Speech (TTS)** — Browser `SpeechSynthesis` API for read-aloud per message; voice selection in Settings.

### 3.7 File & Image Understanding
- Images passed to Gemini vision-capable models as inline base64 parts.
- PDFs and DOCX: server-side text extraction (using `pdf-parse` and `mammoth`), then sent as text context.
- Document Q&A: extracted text injected into the conversation context window.
- Upload size limits: Images ≤ 20 MB, Documents ≤ 50 MB.
- Server-side MIME validation and malware check (content-type + magic bytes).
- Files stored in Supabase Storage under `users/{userId}/attachments/` with RLS restricting access to the owner.

### 3.8 Memory & Context Management
- **Short-Term Context** — Rolling conversation window (last N messages that fit within the model's context budget).
- **Long-Term Memory Engine** — After every conversation turn, a background Server Action checks for extractable user facts (preferences, goals, biographical details). Facts are embedded and stored in the `Memory` table.
- **RAG Retrieval** — Before each Gemini call, the top-3 semantically relevant memories are retrieved via pgvector cosine similarity and injected under a `<context_memories>` tag in the system prompt.
- **Memory Inspector** — Users can view, edit labels, and delete individual memory entries from the Settings → Memory page.
- **Temporary Chat Exception** — Memory extraction is completely disabled for temporary chat sessions.

### 3.9 Personalization
- **Response Style Presets** — Professional, Friendly, Warm (Default), Candid, Direct, Academic, Creative, Concise, Detailed.
- **Tone Controls** — Warmth slider (Less Warm → Default → More Warm), Formality, Enthusiasm, Directness, Detail Level, Emoji Frequency.
- **Formatting Preferences** — Default, More Structured, Less Structured, Minimal Formatting.
- **Custom Instructions** — Free-text box stored per user; always prepended to the system prompt on every Gemini request.
- These preferences are stored in `UserPreference` and applied server-side to every AI request; they are never optional or decorative.

### 3.10 Session Organization & Search
- **Conversation History Sidebar** — Grouped chronologically.
- **Search** — Supabase full-text search on `conversations.title` and `messages.content`. Results link directly to the matching conversation and scroll to the matching message.
- **Pinning** — Pinned conversations shown above recents with a pin icon badge.
- **Archiving** — Archived conversations hidden from main list; visible under Archive section.
- **Rename** — Inline edit via the context menu.
- **Delete** — Soft delete with confirmation modal; hard-deletes on a 30-day schedule or immediately on account deletion.
- **Export** — Export single conversation as Markdown, JSON, or PDF (using `jsPDF`).

### 3.11 Web Search & Library Search
- **Web Search** — Toggleable from Settings → General. Uses a configured search API (e.g., Brave Search, SerpAPI, or Tavily). Results injected as cited context. Sources shown as numbered inline citations with clickable URLs.
- **Library Search** — Semantic search over user's uploaded documents using pgvector embeddings of extracted document text. Results are private to the authenticated user via RLS.

### 3.12 Profile & Account Management
- **Profile Page** — Avatar upload (Supabase Storage), Full Name, Username, Email, Phone, Account creation date.
- **My MEENA Section** — Personalization summary, Memory status, Custom instructions preview.
- **Account Menu** — My Profile, Settings, Add Account, Switch Account, Upgrade Plan, Log Out.
- **Account Switching** — Multiple Supabase Auth sessions supported; switch without full re-authentication where the provider permits.

### 3.13 Settings (Full Specification)

#### Appearance
- Light Mode, Dark Mode, System Default (immediate full-application update, persisted to `UserPreference`).

#### Accent Colors
- Pink (Default), Lavender, Blue, Green, Peach, Rose, Grey, Custom (hex picker). The selected accent updates buttons, focus rings, active states, and highlights across the entire application via CSS custom properties.

#### Typography
- Font Size: Small (14px base), Default (15px base), Large (17px base).
- Font Family: Plus Jakarta Sans (Default), Inter, System Default.

#### General
- Your Name, App Language, Recent Photos toggle, Visual Answers toggle, Home Page Suggestions toggle, Web Search toggle, Library Search toggle, Notifications toggle.

#### Intelligence
- Fast Answers (`gemini-2.0-flash`, lower temperature), Detailed Answers (`gemini-2.5-pro`, higher token budget), Balanced Answers (default), Context-Aware Responses (RAG fully enabled).

#### Voice
- Voice Mode: Standard (SpeechSynthesis), Live (future), Modal (future). Clearly marked as Available / Coming Soon.
- Voice Selection (platform-available voices listed).
- Speech Speed slider.
- Voice Language selector.
- Enable/Disable Spoken Responses toggle.

#### Language
- Interface Language, AI Response Language, Speech Recognition Language, TTS Language. Supports Indian (Hindi, Tamil, Telugu, Bengali, Kannada, Marathi, Gujarati, Punjabi, Malayalam, Odia) and major international languages where Google APIs support them.

#### Background Conversations
- Toggle: allow conversations to continue processing while navigating. Clearly explains browser tab lifecycle limitations.

#### Default Assistant
- Web: "Open MEENA in a new tab" link. Explains that setting a website as a default Android assistant requires a native Android application and cannot be done from a web browser. No false claims.

#### Login & Security
- Login Methods (connected providers list), Passkeys & Security Keys (register/remove), Active Sessions (device list with revoke), Multi-Factor Authentication, Account Recovery codes.

#### Privacy Center
- Memory Controls, Data Collection Preferences, Data Export (full GDPR-style JSON export), Account Deletion (permanent, with 30-day grace period).

#### Storage
- Storage Usage (chart), Uploaded Files (list with delete), Storage Limit display.

#### History & Data
- Conversation History, Archived Conversations, Temporary Chat info, Delete All History, Export All History.

#### Subscription & Usage
- Current Plan, Renewal Date, Billing History. Usage: Total Messages, AI Requests, File Uploads, Voice Usage, Remaining Quota. All figures from real `UsageRecord` table rows.

#### About MEENA
- Version, Project Description, Terms of Service, Privacy Policy, Contact & Support.

### 3.14 Upgrade / Subscription Plans

| Feature | Free | Plus | Pro |
| :--- | :--- | :--- | :--- |
| Messages / day | 50 | 500 | Unlimited |
| Models | Flash | Flash + Pro | Flash + Pro |
| File uploads | 5 / day | 50 / day | 200 / day |
| Voice usage | Standard | Standard | Standard + Live (future) |
| Memory | Basic | Full | Full + Priority |
| Web Search | — | ✓ | ✓ |
| Library Search | — | ✓ | ✓ |

> Billing integration (Stripe or Razorpay) is a future configuration requirement. Do not display active payment UI until a real billing provider is connected.

---

## 4. Frontend & Backend Coding Standards

### 4.1 General Principles
1. **DRY & Single Responsibility** — Functions and components must do one thing well.
2. **Explicit Over Clever** — Prefer readable, maintainable code over dense one-liners.
3. **Zero Untyped Values** — Never use `any`. Use strict TypeScript interfaces, type aliases, or Zod schemas for every boundary.
4. **Defensive Programming** — Validate all user and API inputs at system boundaries using `zod`.
5. **No Secrets in Client Code** — All API keys, service role keys, and credentials live exclusively in server-side environment variables. Never import them into `'use client'` components.

### 4.2 Frontend Architecture Standards

**Component File Structure:**
```
src/
├── app/                        # Next.js App Router pages, layouts, route handlers
│   ├── (auth)/                 # Auth pages: login, signup, verify, reset
│   ├── (app)/                  # Protected app shell
│   │   ├── chat/[id]/          # Conversation page
│   │   ├── temporary/          # Temporary chat page
│   │   ├── profile/            # Profile management
│   │   ├── settings/           # Settings (all subsections)
│   │   └── upgrade/            # Subscription / pricing page
│   └── share/[shareId]/        # Public read-only shared conversation
├── components/
│   ├── ui/                     # Atomic primitives: Button, Input, Card, Modal, Badge, Tooltip
│   ├── chat/                   # MessageList, MessageBubble, ChatInput, MessageActions
│   ├── layout/                 # Sidebar, Header, NavigationDrawer, AccountMenu
│   ├── settings/               # Settings section components
│   └── shared/                 # ThemeToggle, Avatar, MarkdownRenderer, CodeBlock
├── hooks/                      # useChatStream, useAudioRecorder, useTheme, useAccentColor
├── lib/
│   ├── gemini.ts               # Gemini API client (server-only)
│   ├── supabase/               # Supabase server + browser clients
│   ├── ml-client.ts            # FastAPI ML service client
│   ├── rate-limiter.ts         # Token bucket implementation
│   └── utils/                  # sanitize, format, parse helpers
├── stores/                     # Zustand: chatStore, uiStore, settingsStore, authStore
└── types/                      # Shared TypeScript interfaces and Zod schemas
```

**Component Conventions:**
- Server Components by default; add `'use client'` only when state, effects, or browser APIs are explicitly needed.
- Avoid large monolithic components. The chat input, for example, must be decomposed into: `ComposerToolbar`, `ComposerTextarea`, `AttachmentPreview`, and `ComposerActions`.
- Use semantic color tokens from `brandGuidelines.md` exclusively (e.g., `bg-surface-light dark:bg-surface-dark`). Never hardcode hex values directly in component `className` strings.

**Accessibility (a11y):**
- All interactive elements must have accessible labels (`aria-label`, `aria-describedby`, `role`).
- Full keyboard navigation: `Tab`/`Shift+Tab`, `Esc` closes modals, `Enter` sends, `Shift+Enter` adds newlines.
- Respect `prefers-reduced-motion: reduce` — replace positional transforms with simple opacity fades.
- Minimum touch target: 44 × 44 px on all interactive icons.

### 4.3 Backend & API Standards

**Standardized Response Envelope** (all non-streaming routes):
```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;       // e.g. "UNAUTHORIZED", "RATE_LIMITED", "INVALID_INPUT"
    message: string;    // human-readable, safe for client display
    details?: unknown;  // debug-only, never in production
  };
  timestamp: string;    // ISO 8601
}
```

**Error Handling:**
- Catch and transform all internal errors into sanitized client-safe messages.
- Never expose raw database query text, connection strings, stack traces, or service keys.
- Log full errors server-side with `timestamp`, `route`, `userId` (if authenticated), and `durationMs`.

**Rate Limiting:**
- IP-based token bucket for unauthenticated routes: 10 req/min.
- User-based token bucket for authenticated routes: 20 req/min (Free), 60 req/min (Plus), 120 req/min (Pro).
- Implemented in `src/lib/rate-limiter.ts`, applied in Next.js middleware.

---

## 5. Database Schema (Prisma / PostgreSQL)

> All tables must have Row Level Security (RLS) policies enabled in Supabase. Users may only read and write their own records.

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}

generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["postgresqlExtensions"]
}

extensions {
  pgvector(map: "vector")
  pg_trgm()
  unaccent()
}

// ─────────────────────────────────────────
// AUTHENTICATION & IDENTITY
// ─────────────────────────────────────────

model User {
  id            String    @id @default(cuid())
  supabaseId    String    @unique           // Maps to Supabase auth.users.id
  email         String?   @unique
  emailVerified DateTime?
  phone         String?   @unique
  phoneVerified DateTime?
  name          String?
  username      String?   @unique
  avatarUrl     String?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  deletedAt     DateTime?                  // Soft delete; hard-purge after 30 days

  conversations  Conversation[]
  memories       Memory[]
  preferences    UserPreference?
  attachments    Attachment[]
  sharedLinks    SharedConversation[]
  usageRecords   UsageRecord[]
  deviceSessions DeviceSession[]
  mlFeedback     MLFeedback[]

  @@index([supabaseId])
  @@index([email])
}

// ─────────────────────────────────────────
// CONVERSATIONS & MESSAGES
// ─────────────────────────────────────────

model Conversation {
  id           String    @id @default(cuid())
  userId       String
  title        String    @default("New Conversation")
  isPinned     Boolean   @default(false)
  isArchived   Boolean   @default(false)
  isTemporary  Boolean   @default(false)   // Ephemeral sessions — not persisted long-term
  deletedAt    DateTime?                   // Soft delete
  createdAt    DateTime  @default(now())
  updatedAt    DateTime  @updatedAt

  user         User              @relation(fields: [userId], references: [id], onDelete: Cascade)
  messages     Message[]
  sharedLinks  SharedConversation[]

  @@index([userId, updatedAt])
  @@index([userId, isPinned])
  @@index([userId, isArchived])
}

model Message {
  id             String       @id @default(cuid())
  conversationId String
  role           MessageRole
  content        String
  contentHtml    String?      // Pre-rendered safe HTML for display (optional cache)
  tokens         Int?
  model          String?      // e.g. "gemini-2.0-flash"
  branchIndex    Int          @default(0)  // For message branching / regeneration
  parentId       String?                  // Parent message for branching tree
  isEdited       Boolean      @default(false)
  metadata       Json?        // { attachmentIds, emotionTag, intentLabel, sentimentLabel }
  createdAt      DateTime     @default(now())
  updatedAt      DateTime     @updatedAt

  conversation   Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  attachments    Attachment[]
  feedback       MLFeedback[]

  @@index([conversationId, createdAt])
  @@index([conversationId, branchIndex])
}

enum MessageRole {
  USER
  ASSISTANT
  SYSTEM
}

// ─────────────────────────────────────────
// ATTACHMENTS
// ─────────────────────────────────────────

model Attachment {
  id             String   @id @default(cuid())
  userId         String
  messageId      String?
  fileName       String
  mimeType       String
  sizeBytes      Int
  storagePath    String   // Supabase Storage path: users/{userId}/attachments/{filename}
  extractedText  String?  // Extracted text from PDFs / DOCX
  createdAt      DateTime @default(now())

  user           User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  message        Message? @relation(fields: [messageId], references: [id], onDelete: SetNull)

  @@index([userId])
  @@index([messageId])
}

// ─────────────────────────────────────────
// SHARED CONVERSATIONS
// ─────────────────────────────────────────

model SharedConversation {
  id             String    @id @default(cuid())
  conversationId String
  userId         String
  shareToken     String    @unique @default(cuid())
  isActive       Boolean   @default(true)
  viewCount      Int       @default(0)
  createdAt      DateTime  @default(now())
  expiresAt      DateTime?

  conversation   Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  user           User         @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([shareToken])
  @@index([userId])
}

// ─────────────────────────────────────────
// LONG-TERM MEMORY (pgvector RAG)
// ─────────────────────────────────────────

model Memory {
  id          String    @id @default(cuid())
  userId      String
  category    MemoryCategory
  content     String
  embedding   Unsupported("vector(3072)")?  // gemini-embedding-exp-03-07 output dimension
  importance  Int       @default(1)         // 1 (low) to 5 (high)
  source      String?   // conversationId that generated this memory
  isDeleted   Boolean   @default(false)
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt

  user        User      @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@index([userId, category])
}

enum MemoryCategory {
  PREFERENCE
  FACT
  EMOTIONAL_GOAL
  TOPIC
  SKILL
  RELATIONSHIP
}

// ─────────────────────────────────────────
// USER PREFERENCES
// ─────────────────────────────────────────

model UserPreference {
  id                   String   @id @default(cuid())
  userId               String   @unique

  // Appearance
  theme                String   @default("system")       // "light" | "dark" | "system"
  accentColor          String   @default("rose")         // "rose" | "lavender" | "blue" | "green" | "peach" | "grey" | hex
  fontFamily           String   @default("plus-jakarta") // "plus-jakarta" | "inter" | "system"
  fontSize             String   @default("default")      // "small" | "default" | "large"

  // Intelligence
  intelligenceMode     String   @default("balanced")     // "fast" | "balanced" | "detailed" | "context-aware"
  primaryModel         String   @default("gemini-2.0-flash")
  temperature          Float    @default(0.7)

  // Personalization
  responseStyle        String   @default("warm")
  warmthLevel          Int      @default(2)              // 1 (less) to 3 (more)
  formalityLevel       Int      @default(2)              // 1–5
  enthusiasmLevel      Int      @default(3)              // 1–5
  directnessLevel      Int      @default(3)              // 1–5
  detailLevel          Int      @default(3)              // 1–5
  emojiFrequency       Int      @default(1)              // 0 (none) to 3 (frequent)
  formattingStyle      String   @default("default")

  // Memory
  enableMemory         Boolean  @default(true)
  memoryConsent        Boolean  @default(false)          // Explicit consent for memory extraction

  // Custom Instructions
  customInstructions   String?  @db.Text

  // Voice
  speechVoice          String?
  speechSpeed          Float    @default(1.0)
  voiceLanguage        String   @default("en-US")
  enableVoiceResponses Boolean  @default(false)

  // Language
  interfaceLanguage    String   @default("en")
  aiResponseLanguage   String   @default("en")
  sttLanguage          String   @default("en-US")

  // General
  webSearchEnabled     Boolean  @default(false)
  librarySearchEnabled Boolean  @default(false)
  visualAnswers        Boolean  @default(true)
  homeSuggestions      Boolean  @default(true)
  notificationsEnabled Boolean  @default(true)

  updatedAt            DateTime @updatedAt

  user                 User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}

// ─────────────────────────────────────────
// USAGE TRACKING
// ─────────────────────────────────────────

model UsageRecord {
  id          String   @id @default(cuid())
  userId      String
  date        DateTime @default(now()) @db.Date
  messages    Int      @default(0)
  aiRequests  Int      @default(0)
  fileUploads Int      @default(0)
  voiceUsage  Int      @default(0)   // seconds
  tokensIn    Int      @default(0)
  tokensOut   Int      @default(0)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  user        User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([userId, date])
  @@index([userId, date])
}

// ─────────────────────────────────────────
// DEVICE SESSIONS
// ─────────────────────────────────────────

model DeviceSession {
  id          String   @id @default(cuid())
  userId      String
  deviceName  String?
  deviceType  String?  // "desktop" | "mobile" | "tablet"
  ipAddress   String?
  userAgent   String?
  lastSeenAt  DateTime @default(now())
  createdAt   DateTime @default(now())
  isRevoked   Boolean  @default(false)

  user        User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
}

// ─────────────────────────────────────────
// ML FEEDBACK & EVALUATION
// ─────────────────────────────────────────

model MLFeedback {
  id              String   @id @default(cuid())
  userId          String
  messageId       String
  feedbackType    String   // "thumbs_up" | "thumbs_down" | "explicit_rating"
  rating          Int?     // 1–5
  predictedIntent String?
  predictedSentiment String?
  retrievalScore  Float?
  createdAt       DateTime @default(now())

  user            User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  message         Message  @relation(fields: [messageId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@index([messageId])
}
```

---

## 6. Authentication Architecture

### 6.1 Provider: Supabase Auth

Supabase Auth is the single source of truth for all authentication. Auth.js / NextAuth is **not** used in this project. Session tokens are managed by Supabase's built-in session system using `HttpOnly`, `SameSite=Lax`, `Secure` cookies.

### 6.2 Supported Authentication Methods

| Method | Implementation | External Credentials Required |
| :--- | :--- | :--- |
| **Google OAuth** | Supabase → Google Cloud Console OAuth 2.0 app | Google Cloud project with OAuth credentials |
| **Apple OAuth** | Supabase → Apple Developer Sign in with Apple | Apple Developer account + Service ID |
| **Email + Password** | Supabase native | None (Supabase SMTP or external SMTP for emails) |
| **Email OTP** | Supabase native (6-digit OTP sent via email) | SMTP configuration |
| **Email Magic Link** | Supabase native | SMTP configuration |
| **Phone OTP (SMS)** | Supabase + Twilio / MessageBird | Twilio account SID + Auth Token |
| **WebAuthn Passkeys** | Supabase native (requires Supabase ≥ 2.x) | None (browser support required) |

### 6.3 Authentication Flow Requirements
- Registration: email + password with email verification OTP before access is granted.
- Login: email/password, Google, Apple, Magic Link, or Passkey.
- Password Reset: email link → new password form → Supabase `updateUser`.
- Session Refresh: Supabase auto-refreshes tokens; middleware validates on every protected request.
- Session Expiration: configurable via Supabase dashboard (default 1 hour access token, 7-day refresh token).
- Duplicate Account Handling: Supabase returns a clear error; UI surfaces a "This email is already registered" message with a login CTA.
- Secure Logout: `supabase.auth.signOut()` on client; server-side cookie cleared in the logout route handler.
- Never trust client-side password comparisons. Never store plain-text passwords. Never generate fake OTPs.

### 6.4 Passkeys (WebAuthn)
- Register passkey: Supabase `enrollFactor` with FIDO2/WebAuthn.
- Sign in with passkey: Supabase passkey challenge flow.
- Remove passkey: Supabase `unenrollFactor`.
- Hardware security keys (YubiKey etc.) supported where the browser and Supabase implementation permit.
- Document as a configuration requirement if the target Supabase project version does not support it.

### 6.5 Security Dashboard
- Active Sessions list (from `DeviceSession` table): device name, type, IP, last seen.
- Revoke individual sessions.
- Recent Login History.
- MFA status and enrollment.
- Account Recovery codes.
- Security recommendations (unverified email, no MFA, old sessions).

### 6.6 Prompt Injection Defense
- User messages are never directly interpolated into the system prompt string.
- All user content is wrapped in explicit delimiters before being passed to Gemini: `<user_message>...</user_message>`.
- Server-side input validation with Zod rejects oversized payloads and strips null bytes.
- Automated content moderation check on inputs using Gemini's safety settings (`BLOCK_MEDIUM_AND_ABOVE` for harassment, hate speech, sexually explicit content, dangerous content).

---

## 7. AI & LLM Integration

### 7.1 Model Selection

> **Important:** The following model identifiers are correct as of November 2024. Always verify against the [official Google AI model documentation](https://ai.google.dev/gemini-api/docs/models) before releasing.

| Model ID | Use Case | Context Window |
| :--- | :--- | :--- |
| `gemini-2.0-flash` | Default conversational engine, fast responses, daily interactions | 1M tokens |
| `gemini-2.5-pro` | Deep reasoning, long documents, multi-step code, complex analysis | 1M tokens |
| `gemini-embedding-exp-03-07` | Semantic memory embeddings (3072 dimensions) | 8K input tokens |

**Legacy models removed from specification:** `gemini-1.5-flash` and `gemini-1.5-pro` are superseded. `text-embedding-004` has been replaced with `gemini-embedding-exp-03-07`. Do not reference deprecated model IDs in code.

### 7.2 Generation Parameters

| Parameter | Fast Mode | Balanced Mode | Detailed Mode |
| :--- | :--- | :--- | :--- |
| `temperature` | 0.4 | 0.7 | 0.9 |
| `topP` | 0.85 | 0.90 | 0.95 |
| `maxOutputTokens` | 1024 | 2048 | 8192 |

### 7.3 System Prompt Specification

```
You are MEENA, a thoughtful, empathetic, and mindful AI companion.

Core Characteristics:
- Tone: Warm, grounded, attentive, and kind. Write with the grace, clarity, and authenticity of a thoughtful human writer.
- Listening: Always acknowledge the user's emotional undertone before jumping into practical advice.
- Formatting: Format responses cleanly using Markdown. Use spacing and paragraphs generously. Avoid dense walls of text.
- Visuals & Metaphors: Use gentle, vivid descriptions when appropriate, but never sound pretentious or hollow.
- Honesty: When you do not know something, say so with quiet grace. Never hallucinate facts or pretend to have human physical embodiment.
- Adaptation: If the user needs rapid, direct answers (e.g., coding or quick calculations), transition smoothly into concise, structured problem-solving without unnecessary pleasantries.

[INJECTED: custom_instructions — from UserPreference.customInstructions]
[INJECTED: response_style — from UserPreference.responseStyle]
[INJECTED: context_memories — top-3 semantically relevant long-term memories from pgvector]

<user_message>
{sanitized user input}
</user_message>
```

### 7.4 Streaming Implementation

- Use `generateContentStream` from `@google/genai` on the server.
- Route: `POST /api/chat` returns a `ReadableStream` with `Content-Type: text/event-stream`.
- Each SSE event carries a JSON payload: `{ type: "delta" | "done" | "error", content: string }`.
- Client uses `EventSource` or `fetch` with `ReadableStream` to consume the stream.
- Stop generation: client sends `DELETE /api/chat/{streamId}`; server calls `AbortController.abort()`.

### 7.5 Semantic Memory RAG Pipeline

1. **Extraction** — After every conversation turn, a background Server Action (`extractAndStoreMemory`) asks `gemini-2.0-flash` to identify any new extractable user facts (preferences, goals, biographical details). Facts are only extracted if `UserPreference.memoryConsent = true`.
2. **Embedding** — Extracted fact text is embedded using `gemini-embedding-exp-03-07` (3072-dim vector).
3. **Storage** — Vectors stored in the `Memory` table's `embedding` column (`vector(3072)`).
4. **Retrieval** — Before each Gemini call, run: `SELECT content FROM Memory WHERE userId = $1 ORDER BY embedding <=> $2 LIMIT 3` (cosine distance). Similarity threshold: > 0.75.
5. **Context Injection** — Top-3 results injected into the system prompt under `<context_memories>`.
6. **Temporary Chat Exception** — Steps 1–5 are entirely skipped for `isTemporary = true` conversations.

---

## 8. Machine Learning Implementation

> **Distinction:** The ML algorithms in this section are **independently implemented** classical algorithms, completely separate from the Google Gemini API. They are not wrappers around Gemini. They run in a dedicated Python FastAPI microservice and contribute real, measurable functionality to MEENA.

### 8.1 ML Service Architecture

```
ml-service/
├── data/
│   ├── intents_dataset.csv        # Labeled intent classification training data
│   ├── sentiment_dataset.csv      # Labeled sentiment training data
│   └── conversations_sample.json  # Anonymized conversation clusters sample
├── models/
│   ├── intent_classifier/         # Saved TF-IDF vectorizer + Linear SVM pipeline
│   ├── sentiment_classifier/      # Saved TF-IDF vectorizer + Logistic Regression pipeline
│   ├── knn_retriever/             # Saved KNN model + TF-IDF vectorizer
│   └── kmeans_cluster/            # Saved K-Means model + TF-IDF vectorizer
├── training/
│   ├── train_intent.py
│   ├── train_sentiment.py
│   ├── train_knn.py
│   └── train_kmeans.py
├── evaluation/
│   ├── eval_intent.py
│   ├── eval_sentiment.py
│   └── reports/                   # JSON + text evaluation reports with metrics
├── api/
│   └── main.py                    # FastAPI app exposing ML endpoints
├── requirements.txt
└── README.md
```

### 8.2 Algorithm 1 — TF-IDF + Logistic Regression (Sentiment Classification)

**Purpose:** Classify user messages as Positive, Negative, or Neutral sentiment. The result is stored in `Message.metadata.sentimentLabel` and used to adapt MEENA's tone in the system prompt (e.g., more empathetic framing when negative sentiment is detected).

**Dataset:** A labeled sentiment dataset (e.g., cleaned Twitter Sentiment Analysis or SemEval data, minimum 10,000 labeled examples).

**Pipeline:**
```python
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

sentiment_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=20000, ngram_range=(1, 2), sublinear_tf=True)),
    ('clf',   LogisticRegression(C=1.0, max_iter=1000, class_weight='balanced'))
])
```

**Evaluation Metrics:** Accuracy, Precision, Recall, F1-score (macro and per-class). Target: F1 ≥ 0.78 on held-out test set.

**Integration:** `POST /ml/classify-sentiment` → `{ text: string }` → `{ label: "POSITIVE"|"NEGATIVE"|"NEUTRAL", confidence: float }`.

### 8.3 Algorithm 2 — TF-IDF + Linear SVM (Intent Classification)

**Purpose:** Classify user messages into one of MEENA's supported intents (e.g., `GENERAL_CHAT`, `CODE_HELP`, `LANGUAGE_PRACTICE`, `DOCUMENT_QA`, `EMOTIONAL_SUPPORT`, `FACTUAL_QUESTION`, `CREATIVE_WRITING`, `MATH_HELP`).

**Dataset:** Curated intent dataset built from existing labeled conversational corpora (e.g., HWU64, CLINC150 subsets) plus MEENA-specific intent labels.

**Pipeline:**
```python
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

intent_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=25000, ngram_range=(1, 3), sublinear_tf=True)),
    ('clf',   CalibratedClassifierCV(LinearSVC(C=0.5, max_iter=2000)))
])
```

**Evaluation Metrics:** Accuracy, macro F1-score, per-intent precision and recall. Target: Accuracy ≥ 0.82, macro F1 ≥ 0.80.

**Integration:** `POST /ml/classify-intent` → `{ text: string }` → `{ intent: string, confidence: float, top3: [...] }`.

**Usage in MEENA:** The predicted intent is stored in `Message.metadata.intentLabel` and used to route the conversation to the optimal Gemini model (e.g., `CODE_HELP` and `MATH_HELP` automatically select `gemini-2.5-pro`).

### 8.4 Algorithm 3 — TF-IDF + Cosine Similarity / KNN (Semantic Context Retrieval)

**Purpose:** Retrieve the most semantically similar past conversation excerpts or FAQ entries to include as few-shot context examples in the Gemini prompt, improving response relevance for recurring question patterns.

**Approach A — TF-IDF Cosine Similarity:**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# At query time:
query_vec = vectorizer.transform([user_message])
scores = cosine_similarity(query_vec, corpus_matrix)
top_k_indices = scores.argsort()[0][-5:][::-1]
```

**Approach B — K-Nearest Neighbors:**
```python
from sklearn.neighbors import NearestNeighbors

knn = NearestNeighbors(n_neighbors=5, metric='cosine', algorithm='brute')
knn.fit(corpus_matrix)
distances, indices = knn.kneighbors(query_vec)
```

**Integration:** `POST /ml/similar-contexts` → `{ text: string, top_k: int }` → `{ results: [{ text, score }] }`.

**Note:** For production-quality semantic retrieval, Sentence Transformers (`all-MiniLM-L6-v2` or `paraphrase-multilingual-MiniLM-L12-v2`) are used alongside TF-IDF as a hybrid retrieval fallback when pgvector memory is unavailable.

### 8.5 Algorithm 4 — K-Means Clustering (Topic Analysis)

**Purpose:** Cluster anonymized conversation topics to identify common themes across the user base. Used by the MEENA team to understand what users discuss most and to curate better home page suggestions. No PII is included in clustering inputs.

**Pipeline:**
```python
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD

# TF-IDF + dimensionality reduction + clustering
tfidf = TfidfVectorizer(max_features=15000, stop_words='english', sublinear_tf=True)
svd = TruncatedSVD(n_components=100, random_state=42)
kmeans = KMeans(n_clusters=20, random_state=42, n_init=10)
```

**Evaluation Metrics:** Inertia (elbow method), Silhouette Score (target ≥ 0.35), top-N keywords per cluster.

**Integration:** `GET /ml/cluster-topics` → `{ clusters: [{ id, keywords, size }] }`. Admin-only endpoint; not user-facing.

### 8.6 Feedback-Based Evaluation Mechanism

**Purpose:** Use thumbs-up / thumbs-down feedback from users to continuously evaluate the quality of ML predictions and Gemini responses. Adjust retrieval ranking weights over time based on accumulated feedback.

**Implementation:**
1. When a user clicks Thumbs Down on a MEENA response, the `MLFeedback` record is written with the message ID, intent label, sentiment label, and retrieval score.
2. A weekly offline evaluation script reads `MLFeedback` records and computes: mean retrieval score for positive feedback vs. negative feedback. Where retrieval quality consistently underperforms, the similarity threshold or top-k parameter is adjusted.
3. Feedback data is aggregated only; individual user messages are never used to retrain models without explicit opt-in consent.

**Endpoint:** `POST /ml/feedback` → `{ messageId, feedbackType, rating }`.

### 8.7 ML Evaluation Report Structure

Each training run must produce a report saved to `ml-service/evaluation/reports/`:

```json
{
  "model": "intent_classifier",
  "trainedAt": "ISO-8601 timestamp",
  "trainSize": 8000,
  "testSize": 2000,
  "accuracy": 0.84,
  "macroF1": 0.82,
  "perClassMetrics": {
    "GENERAL_CHAT": { "precision": 0.91, "recall": 0.89, "f1": 0.90 },
    "CODE_HELP":    { "precision": 0.87, "recall": 0.85, "f1": 0.86 }
  },
  "confusionMatrix": [[...]]
}
```

---

## 9. Step-by-Step Development Workflow

```
[Phase 1] Project Inspection & Documentation
   ├── Inspect existing files and directory structure
   ├── Read Gemini.md and brandGuidelines.md (this file)
   └── Define architecture decisions for the specific project context

[Phase 2] Design System & UI Foundation
   ├── Configure Tailwind CSS v4 with brand tokens (from brandGuidelines.md)
   ├── Set up CSS custom properties for theming and accent colors
   ├── Build atomic component library (Button, Input, Card, Badge, Modal, Tooltip)
   ├── Implement ThemeProvider (light/dark/system) + AccentColorProvider
   └── Build layout shell: Sidebar, Header, Main Canvas — responsive at all breakpoints

[Phase 3] Core Chat Interface & Streaming
   ├── Chat input (ComposerTextarea, ComposerToolbar, AttachmentPreview, ComposerActions)
   ├── SSE route handler at POST /api/chat
   ├── Gemini SDK integration with streaming + AbortController stop
   ├── MessageList: MessageBubble (user/assistant), MessageActions, BranchNavigator
   ├── MarkdownRenderer with KaTeX + Shiki code blocks + copy button
   └── Optimistic client state updates with Zustand chatStore

[Phase 4] Authentication & Database
   ├── Supabase Auth: Google OAuth, Apple OAuth, Email+Password, OTP, Magic Link
   ├── WebAuthn Passkey registration and login
   ├── Prisma schema migration and Supabase RLS policies
   ├── Auth middleware (validate session on every protected route)
   ├── User profile creation on first login
   └── DeviceSession tracking

[Phase 5] Conversation Persistence & Sidebar
   ├── Conversation CRUD: create, rename, pin, archive, delete, restore
   ├── Auto-title generation using Gemini on the first message
   ├── Sidebar with chronological grouping and conversation context menu
   ├── Full-text search: POST /api/conversations/search
   ├── Shared conversation links: generate, revoke, public read-only view
   └── Message editing and branch navigation

[Phase 6] Attachments, Voice & Multimodal
   ├── File upload: Supabase Storage + server-side text extraction
   ├── Image upload: passed to Gemini as vision parts
   ├── Attachment preview strip in composer
   ├── Voice input: Web Speech API + live transcription
   ├── Voice output: SpeechSynthesis API + voice settings
   └── Temporary Chat: ephemeral server-side session, no DB persistence

[Phase 7] Long-Term Memory & Personalization
   ├── Memory extraction Server Action (post-turn, background)
   ├── pgvector embedding storage with gemini-embedding-exp-03-07
   ├── RAG retrieval pipeline on every Gemini call
   ├── Memory Inspector UI in Settings
   ├── Custom Instructions saved to UserPreference and applied to every request
   └── All personalization controls (style, tone, formatting, language)

[Phase 8] Settings, Profile & Account Management
   ├── Settings page with all subsections (see Section 3.13)
   ├── Profile page with avatar upload
   ├── Account switching and multi-account support
   ├── Security dashboard (sessions, MFA, passkeys)
   ├── Usage records display from UsageRecord table
   ├── Privacy Center: data export, account deletion
   └── Upgrade / Subscription page

[Phase 9] Machine Learning Service
   ├── Set up Python FastAPI ml-service
   ├── Prepare and curate training datasets
   ├── Train and evaluate all four ML algorithms
   ├── Save model artifacts and generate evaluation reports
   └── Integrate ML predictions into the Next.js chat pipeline

[Phase 10] Web Search & Library Search
   ├── Configure external search API (Brave / SerpAPI / Tavily)
   ├── Web search context injection into Gemini prompt with citations
   ├── Library search: embed uploaded document text + pgvector similarity search
   └── Search result formatting in the chat UI

[Phase 11] QA, Hardening & Production Polish
   ├── Vitest unit tests for utilities, hooks, and ML client
   ├── React Testing Library component tests for critical UI flows
   ├── Playwright E2E tests covering all 35 test scenarios (see Section 11)
   ├── Accessibility audit (WCAG 2.1 AA compliance)
   ├── Lighthouse score targets: Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 95
   └── Security audit: RLS policy verification, rate limit testing, injection testing
```

---

## 10. Testing, Debugging & Quality Assurance

### 10.1 Automated Test Suites
- **Unit Testing** (Vitest + RTL): Core helpers, message formatting, ML client, memory extraction parser, Zod schemas, custom hooks.
- **API Route Testing**: Mock Gemini responses to verify SSE streaming, rate limit triggers, auth guards, and error response shapes.
- **E2E Testing** (Playwright): Full browser automation against a local dev instance with a seeded test database.

### 10.2 E2E Test Checklist (Playwright)
1. Sign-up with email + password.
2. Email OTP verification.
3. Google OAuth login.
4. Password reset flow.
5. Passkey registration and login.
6. Create a new conversation.
7. Send a message and receive a real Gemini AI response.
8. Stop streaming mid-response.
9. Edit a user message and verify regeneration.
10. Regenerate an assistant response.
11. Copy a message to clipboard.
12. Share a conversation — generate and copy link.
13. Revoke a shared link.
14. Pin and unpin a conversation.
15. Archive and restore a conversation.
16. Rename a conversation.
17. Delete a conversation (with confirmation modal).
18. Search conversation history.
19. Upload an image attachment.
20. Upload a PDF and ask a document question.
21. Voice input recording and transcription.
22. Activate Temporary Chat; verify no sidebar entry is created.
23. Edit profile name and avatar.
24. Apply personalization settings; verify system prompt changes.
25. Toggle memory on/off; verify extraction is skipped when off.
26. Switch between light and dark themes.
27. Change accent color; verify UI updates.
28. Change accent back to pink (default).
29. Add a second account and switch between accounts.
30. Logout and verify session is cleared.
31. Mobile: verify sidebar drawer opens and closes correctly.
32. Mobile: verify chat input is accessible above safe area.
33. Database persistence: messages survive page reload.
34. User data isolation: user A cannot access user B's conversations.
35. ML endpoint: `POST /ml/classify-intent` returns a valid response.

### 10.3 Observability & Debugging
- Structured JSON server logs: `{ timestamp, route, userId, conversationId, durationMs, status }`.
- Never log raw user message content or memory values in production.
- Dev-only debug panel: Gemini token usage, latency, active RAG memory chunks, ML predictions, intent label.

---

## 11. Developer Onboarding & Contribution Rules

1. **Read First** — Read both [`Gemini.md`](./Gemini.md) and [`brandGuidelines.md`](./brandGuidelines.md) completely before writing or modifying any code.
2. **Follow Brand Tokens** — Never introduce hardcoded hex values, raw Tailwind colors outside the defined palette, or unvetted third-party UI libraries without approval.
3. **No Fake Features** — Every user-visible feature must have a real backend implementation or be clearly labelled "Coming Soon" in the UI with no functional controls.
4. **No Secrets in Client** — Never import `.env` variables that begin with `SUPABASE_SERVICE_ROLE`, `GEMINI_API_KEY`, or similar privileged values into `'use client'` files.
5. **Commit Cleanly** — Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
6. **Type Check** — Every PR must pass `pnpm tsc --noEmit` and `pnpm lint` with zero errors or warnings before merge.
7. **Test Coverage** — New features must be accompanied by unit tests (Vitest) and, for user-facing flows, an E2E scenario (Playwright).
8. **Environment Variables** — Document every new environment variable in `.env.example` with a comment describing what it is and where to obtain it.

---

## 12. Environment Variables Reference

```bash
# ─── Supabase ───────────────────────────────────────────────────────────────
NEXT_PUBLIC_SUPABASE_URL=              # Supabase project URL (safe for client)
NEXT_PUBLIC_SUPABASE_ANON_KEY=         # Supabase anon key (safe for client)
SUPABASE_SERVICE_ROLE_KEY=             # Service role key — SERVER ONLY, never expose

# ─── Database ───────────────────────────────────────────────────────────────
DATABASE_URL=                          # Prisma connection pool URL
DIRECT_URL=                            # Prisma direct connection (for migrations)

# ─── Google Gemini ───────────────────────────────────────────────────────────
GEMINI_API_KEY=                        # Google AI Studio API key — SERVER ONLY

# ─── ML Service ──────────────────────────────────────────────────────────────
ML_SERVICE_URL=http://localhost:8000   # FastAPI ML microservice base URL
ML_SERVICE_API_KEY=                    # Internal shared secret for ML service auth

# ─── External Search (Optional) ──────────────────────────────────────────────
SEARCH_PROVIDER=                       # "brave" | "serpapi" | "tavily"
BRAVE_SEARCH_API_KEY=                  # Brave Search API key (if provider=brave)
SERPAPI_KEY=                           # SerpAPI key (if provider=serpapi)
TAVILY_API_KEY=                        # Tavily API key (if provider=tavily)

# ─── OAuth Providers ─────────────────────────────────────────────────────────
# Configure via Supabase Auth dashboard — these are set in Supabase, not .env
# GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET → Supabase Auth → Providers → Google
# APPLE_CLIENT_ID etc. → Supabase Auth → Providers → Apple

# ─── Phone OTP (Optional) ─────────────────────────────────────────────────────
# Configure via Supabase Auth dashboard → Phone → Twilio
# TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_VERIFY_SID → Supabase dashboard only

# ─── Application ─────────────────────────────────────────────────────────────
NEXT_PUBLIC_APP_URL=http://localhost:3000   # Public base URL for share links
NODE_ENV=development
```
