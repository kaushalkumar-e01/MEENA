# MEENA — Brand & Visual Identity Guidelines

> **CORE DESIGN DIRECTIVE:**
> MEENA's visual identity is **warm, human-designed, minimal, and mindful**.
> We deliberately reject the cold, hyper-saturated, robotic aesthetics common in generic AI applications.
> **Strictly avoid:** neon glowing borders, purple-to-cyan laser gradients, futuristic hologram orbs, floating particles, dizzying parallax tilts, excessive glassmorphism, and gratuitous bouncing animations.
> Every element in MEENA must feel tactile, calm, intentional, and comfortable for long conversational reading sessions.

---

## 1. Brand Philosophy & Aesthetic Identity

| Attribute | What MEENA Is | What MEENA Is NOT |
| :--- | :--- | :--- |
| **Personality** | Empathetic, calm, mindful, welcoming, grounded | Robotic, sterile, hyper-tech, cold, detached |
| **Color Temperature** | Soft warm pastels, gentle rose, creamy earth neutrals | Cold cyber blues, neon purples, harsh terminal greens |
| **Visual Texture** | Matte surfaces, editorial whitespace, quiet 1px borders | Glossy neon glassmorphism, iridescent gradients, thick cartoon borders |
| **Typography** | Elegant, comfortable, book-like legibility, humanist sans | Monospaced "hacker" style, cramped utilitarian typefaces |
| **Motion** | Gentle, quiet ease-out micro-interactions (< 200ms) | Bouncing 3D cards, flashy particle emitters, spinning glow rings |
| **Iconography** | Thin-stroke, consistent Lucide icons (1.5px) | Mixed icon packs, emoji clutter, filled blobby 3D icon sets |
| **Decoration** | Intentional, invisible when unneeded | Random floating shapes, confetti, gamification badges |

---

## 2. Color Palette System

The primary default accent is **Soft Pastel Rose / Pink**. Users may switch the accent color in Settings. All accent variants must meet WCAG 2.1 AA contrast requirements against the surface they appear on.

### 2.1 The Accent Color System

MEENA supports seven named accent colors plus a custom hex option. Each accent is defined as a semantic token scale (50 → 600) using CSS custom properties. The active accent token set is applied globally by the `AccentColorProvider` component.

#### Default Accent: Soft Pastel Rose

| Token Name | Hex | CSS Variable | Usage |
| :--- | :--- | :--- | :--- |
| Rose 50 | `#FDF3F5` | `--accent-50` | User message bubble background (light), active card wash |
| Rose 100 | `#F9E4E8` | `--accent-100` | Chip backgrounds, hover backgrounds, border highlights |
| Rose 200 | `#F4CAD2` | `--accent-200` | Delicate borders, pill active states, soft tags |
| Rose 300 | `#ECA8B7` | `--accent-300` | Focus rings, secondary icon accents |
| Rose 400 | `#DF7B93` | `--accent-400` | **Primary Brand Accent** — active states, dark mode highlights |
| Rose 500 | `#D15E78` | `--accent-500` | CTA button fills (light mode), key interactive icons |
| Rose 600 | `#B94761` | `--accent-600` | Button hover, high-contrast link accents |

#### Lavender Accent

| Token | Hex | Usage |
| :--- | :--- | :--- |
| Lavender 50 | `#F5F3FC` | Light washes |
| Lavender 300 | `#A89BD6` | Focus rings |
| Lavender 400 | `#8B72C8` | **Primary** |
| Lavender 500 | `#7059B5` | Button fills |
| Lavender 600 | `#5A45A0` | Hover |

#### Blue Accent

| Token | Hex | Usage |
| :--- | :--- | :--- |
| Blue 50 | `#EFF6FF` | Light washes |
| Blue 300 | `#93C5FD` | Focus rings |
| Blue 400 | `#60A5FA` | **Primary** |
| Blue 500 | `#3B82F6` | Button fills |
| Blue 600 | `#2563EB` | Hover |

#### Green Accent

| Token | Hex | Usage |
| :--- | :--- | :--- |
| Green 50 | `#F0FDF4` | Light washes |
| Green 300 | `#86EFAC` | Focus rings |
| Green 400 | `#4ADE80` | **Primary** |
| Green 500 | `#22C55E` | Button fills |
| Green 600 | `#16A34A` | Hover |

#### Peach Accent

| Token | Hex | Usage |
| :--- | :--- | :--- |
| Peach 50 | `#FFF7ED` | Light washes |
| Peach 300 | `#FDB77A` | Focus rings |
| Peach 400 | `#FB923C` | **Primary** |
| Peach 500 | `#F97316` | Button fills |
| Peach 600 | `#EA6C0A` | Hover |

#### Grey Accent

| Token | Hex | Usage |
| :--- | :--- | :--- |
| Grey 50 | `#F9FAFB` | Light washes |
| Grey 300 | `#9CA3AF` | Focus rings |
| Grey 400 | `#6B7280` | **Primary** |
| Grey 500 | `#4B5563` | Button fills |
| Grey 600 | `#374151` | Hover |

#### CSS Custom Properties Implementation

```css
/* Defined in src/app/globals.css — overridden by AccentColorProvider */
:root {
  --accent-50:  #FDF3F5;  /* Rose default */
  --accent-100: #F9E4E8;
  --accent-200: #F4CAD2;
  --accent-300: #ECA8B7;
  --accent-400: #DF7B93;
  --accent-500: #D15E78;
  --accent-600: #B94761;
}
/* Each accent preset overrides these six variables only. */
/* All component styles reference var(--accent-*) exclusively. */
```

---

### 2.2 Light Theme Palette — Alabaster Linen & Warm Espresso

Designed like high-quality matte stationery: warm, soft on the eyes, devoid of blinding pure whites or harsh stark contrasts.

```
+--------------------------------------------------------------------------+
|  LIGHT THEME — SURFACE & TEXT TOKENS                                     |
|                                                                          |
|  [ #FAF7F2 ] --bg-base          Warm Alabaster Linen (page background)  |
|  [ #FFFFFF ] --bg-surface       Pure Matte White (cards, chat bubbles)   |
|  [ #F2ECE6 ] --bg-subdued       Soft Oatmeal Wash (sidebar, inset wells) |
|  [ #E7DFD7 ] --border-subtle    Warm Sandstone (1px dividers, hairlines)  |
|  [ #D4C9C0 ] --border-strong    Deeper Neutral (defined component edges)  |
|  [ #2A2325 ] --text-primary     Deep Espresso Noir   (WCAG: 14.5:1)      |
|  [ #63585C ] --text-secondary   Warm Charcoal Slate  (WCAG:  7.2:1)      |
|  [ #9B8E93 ] --text-muted       Soft Heather Neutral (WCAG:  4.6:1)      |
+--------------------------------------------------------------------------+
```

**Semantic Notes:**
- `--bg-base` (`#FAF7F2`): The foundational page canvas. Never replaced with pure `#FFFFFF`.
- `--bg-surface` (`#FFFFFF`): Reserved for elevated cards, modals, and the message input bar.
- `--bg-subdued` (`#F2ECE6`): Sidebar background, inactive chips, inset wells, code block backgrounds.
- `--border-subtle` (`#E7DFD7`): 1px hair-thin borders. The majority of structural lines use this.
- `--text-primary` (`#2A2325`): Warm espresso brown-black. Eliminates eye strain vs. `#000000`.

---

### 2.3 Dark Theme Palette — Velvet Espresso Noir & Cashmere Glow

Built from deep warm espresso undertones rather than cold blue-grays. Feels like a cozy, dimly lit reading study — not an OLED sci-fi simulator.

```
+--------------------------------------------------------------------------+
|  DARK THEME — SURFACE & TEXT TOKENS                                      |
|                                                                          |
|  [ #161214 ] --bg-base          Deep Velvet Espresso (page background)   |
|  [ #1F191C ] --bg-surface       Elevated Cocoa Charcoal (cards, bubbles) |
|  [ #292226 ] --bg-subdued       Soft Muted Heather Well (sidebar, wells)  |
|  [ #382F34 ] --border-subtle    Quiet Charcoal Border (hairlines)         |
|  [ #4A3E45 ] --border-strong    Defined Component Border                  |
|  [ #F5ECEF ] --text-primary     Warm Cashmere Cream   (WCAG: 15.1:1)     |
|  [ #BDB0B6 ] --text-secondary   Soft Taupe Heather    (WCAG:  8.3:1)     |
|  [ #82757C ] --text-muted       Muted Shadow Stone    (WCAG:  4.5:1)     |
+--------------------------------------------------------------------------+
```

**Semantic Notes:**
- `--bg-base` (`#161214`): Deep, restful velvet with a hint of warm undertone.
- `--bg-surface` (`#1F191C`): Chat bubbles, sidebar items, input containers, and card surfaces.
- `--bg-subdued` (`#292226`): Deeper insets, hover states on surface elements, nested containers.
- Accent glow in dark mode: `--accent-400` (`#DF7B93` for rose default) glows warmly against dark surfaces without glare.
- `--text-primary` (`#F5ECEF`): Soft off-white cream. Avoids harsh blue-white eye fatigue of pure `#FFFFFF`.

---

### 2.4 Semantic Status Colors — Muted Pastels

Never use jarring traffic-light primaries. All semantic colors are gently desaturated:

| Purpose | Light Token | Dark Token | Description |
| :--- | :--- | :--- | :--- |
| **Success** | `#6B9E78` Sage Leaf | `#8FBE9B` Pastel Mint | Calming organic green |
| **Warning** | `#D49557` Warm Ochre | `#E5AB72` Soft Amber | Warm, gentle alert |
| **Error / Destructive** | `#C75656` Terracotta | `#DE7575` Pastel Coral | Clear but non-aggressive |
| **Info** | `#6D8EB8` Cornflower | `#92B1D6` Pastel Sky | Subtle informative blue |

---

## 3. Typography & Hierarchy

### 3.1 Typefaces

| Role | Font | Fallback | Notes |
| :--- | :--- | :--- | :--- |
| **Primary UI** | `Plus Jakarta Sans` | `Inter`, `system-ui`, `sans-serif` | Humanist grotesque; warm open counters, balanced geometry. Default. |
| **Alternative UI** | `Inter` | `system-ui`, `sans-serif` | User-selectable in Settings → Appearance. |
| **Editorial Accent** | `Newsreader` or `Fraunces` | serif | Use sparingly: welcome headings, landing copy, contemplative quotes only. |
| **Code & Mono** | `JetBrains Mono` | `Geist Mono`, `Fira Code`, `monospace` | All code blocks: 14px, line-height 1.6, ligatures enabled. |

Fonts are loaded via `next/font/google`. Self-hosted fallbacks must be provided to avoid layout shift.

### 3.2 Type Scale & Rhythm

| Level | Size | Weight | Line Height | Letter Spacing | Usage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Display** | `2.25rem` / 36px | 600 SemiBold | 1.20 | −0.025em | Hero welcome, feature headers |
| **Heading 1** | `1.75rem` / 28px | 600 SemiBold | 1.25 | −0.020em | View titles, modal titles |
| **Heading 2** | `1.375rem` / 22px | 500 Medium | 1.30 | −0.015em | Section headers, drawer titles |
| **Heading 3** | `1.125rem` / 18px | 500 Medium | 1.35 | −0.010em | Card titles, group dividers |
| **Body Large** | `1.0rem` / 16px | 400 Regular | 1.60 | 0em | Primary chat messages, assistant text |
| **Body Default** | `0.9375rem` / 15px | 400 Regular | 1.55 | 0em | UI labels, input fields, settings items |
| **Small** | `0.8125rem` / 13px | 500 Medium | 1.45 | +0.010em | Timestamps, metadata, tooltips |
| **Micro** | `0.6875rem` / 11px | 600 SemiBold | 1.30 | +0.040em | Status badges, pills (UPPERCASE) |

### 3.3 User-Configurable Font Sizes

Users may choose from three size presets in Settings → Appearance → Font Size:

| Preset | Base Size | Scale Factor |
| :--- | :--- | :--- |
| Small | 14px | 0.875 |
| **Default** | 15px | 1.000 |
| Large | 17px | 1.125 |

The active scale factor is applied via a `font-size` on `<html>` and all `rem` values scale accordingly.

---

## 4. Layout, Spacing & Spatial Geometry

### 4.1 The 8-Point Spatial Grid

All margins, padding, gaps, and layout dimensions follow the 4px / 8px increment scale:

| Token | px | Usage |
| :--- | :--- | :--- |
| `space-1` | 4px | Micro gaps, badge inner padding |
| `space-2` | 8px | Icon-to-text spacing, compact button padding |
| `space-3` | 12px | Input inner padding, toolbar item gaps |
| `space-4` | 16px | Standard component padding, list item gaps |
| `space-6` | 24px | Card inner padding, section separation |
| `space-8` | 32px | Container gutters, chat message vertical separation |
| `space-12` | 48px | Major layout divisions |
| `space-16` | 64px | Collapsed sidebar width |

### 4.2 Layout Architecture & Proportions

| Element | Measurement | Notes |
| :--- | :--- | :--- |
| **Chat Canvas Max Width** | `768px` (`max-w-3xl`) | No line of text extends beyond ~75 characters |
| **Sidebar Expanded** | `280px` | Desktop default |
| **Sidebar Icon Rail** | `64px` | Collapsed desktop state |
| **Sidebar Mobile** | Full-width drawer | Slides from left; overlays content |
| **Header Height** | `56px` | Fixed top bar |
| **Composer Min Height** | `52px` | Auto-grows to `200px` before scrolling |
| **Bottom Safe Margin** | `24px` | Between composer and viewport edge |

### 4.3 Corner Radii — Soft Rounded Geometry

| Element Class | Radius | Tailwind | Usage |
| :--- | :--- | :--- | :--- |
| **Small / Subtle** | 8px | `rounded-lg` | Code snippets, dropdown items, tooltips, context menu rows |
| **Interactive Controls** | 12px | `rounded-xl` | Buttons, text inputs, toast notifications |
| **Containers / Bubbles** | 18px | `rounded-2xl` | Chat bubbles, cards, modals, settings panels |
| **Pills & Avatars** | 9999px | `rounded-full` | Category tags, action pills, avatar circles |

Message bubbles additionally apply directional corner softening:
- **User bubble**: `rounded-2xl rounded-br-sm` (bottom-right corner slightly sharper).
- **Assistant bubble**: `rounded-2xl rounded-tl-sm` (top-left corner slightly sharper, near avatar).

### 4.4 Elevation & Shadows

Avoid dark, aggressive drop shadows. Use diffused ambient occlusions only:

```css
/* Light theme — card and modal ambient */
--shadow-ambient: 0 4px 20px -2px rgba(42, 35, 37, 0.04),
                  0 2px 6px  -1px rgba(42, 35, 37, 0.02);

/* Light theme — elevated hover state */
--shadow-hover:   0 10px 25px -4px rgba(42, 35, 37, 0.07),
                  0 4px  10px -2px rgba(42, 35, 37, 0.03);

/* Dark theme — card and modal ambient */
--shadow-dark:    0 4px 24px -2px rgba(0, 0, 0, 0.35);
```

No `box-shadow` with 0px blur or opaque color is ever used. Shadows exist to suggest elevation, not to draw attention.

---

## 5. Component Styling Specifications

### 5.1 Buttons

#### Primary Action Button (Brand Accent)
```
Light:  bg=var(--accent-500)  text=#FFFFFF  border=none
Dark:   bg=var(--accent-400)  text=#161214  border=none
Hover:  brightness-105, scale-[1.01], transition: 150ms ease-out
Shape:  rounded-xl, h-10 (40px) or h-11 (44px), px-5, font-medium
Focus:  ring-2 ring-offset-2 ring-var(--accent-400)/60
```

#### Secondary Button (Soft Surface)
```
Light:  bg=#FFFFFF    border: 1px solid #E7DFD7  text=#2A2325
Dark:   bg=#1F191C    border: 1px solid #382F34  text=#F5ECEF
Hover Light: bg=#FAF7F2
Hover Dark:  bg=#292226
Shape:  rounded-xl, h-10 or h-11, px-5, font-medium
```

#### Ghost / Text Button
```
bg=transparent
Hover: bg=var(--accent-50)/50 (light) or bg=var(--accent-500)/10 (dark)
text: --text-secondary
Shape: rounded-lg, px-3, py-1.5
```

#### Destructive Button
```
Light:  bg=#C75656    text=#FFFFFF
Dark:   bg=#DE7575    text=#161214
Hover:  brightness-105, scale-[1.01]
```

---

### 5.2 Input Fields & Chat Composer

The chat composer is MEENA's primary interactive threshold. It must feel inviting, serene, and uncluttered.

```
+--------------------------------------------------------------------------+
|  CHAT COMPOSER — VISUAL SPECIFICATION                                    |
|                                                                          |
|  +--------------------------------------------------------------------+  |
|  | (+)  Message MEENA...                                (Mic)  [  ↑ ] |  |
|  +--------------------------------------------------------------------+  |
|  | [ attachment thumbnail × ] [ attachment thumbnail × ]              |  |
|  +--------------------------------------------------------------------+  |
|   Shape: rounded-2xl  Padding: 12px  Border: 1px --border-subtle       |
|   Focus ring: ring-2 ring-var(--accent-300)/40 border-var(--accent-400) |
+--------------------------------------------------------------------------+
```

**All text inputs:**
- Shape: `rounded-xl`, padding `px-4 py-2.5`.
- Border: `1px solid var(--border-subtle)`.
- Focus: `ring-2 ring-var(--accent-300)/40 border-var(--accent-400)` — never default browser blue outline.
- Background: `var(--bg-surface)` (light) / `var(--bg-surface)` (dark).
- Placeholder: `var(--text-muted)`.

**Warm placeholder copy examples:**
- *"Message MEENA..."*
- *"What's on your mind?"*
- *"Ask anything, share a thought, or explore an idea..."*

---

### 5.3 Conversational Message Bubbles

#### User Message Bubble
- Alignment: right-aligned, max-width 85% of chat canvas.
- **Light:** `bg=#F9E4E8`, `border: 1px solid #F4CAD2`, `text=#2A2325`, `rounded-2xl rounded-br-sm`.
- **Dark:** `bg=#2D1F24`, `border: 1px solid #4A303A`, `text=#F5ECEF`, `rounded-2xl rounded-br-sm`.
- Padding: `px-4 py-3`.

#### MEENA Assistant Bubble
- Alignment: left-aligned, preceded by MEENA's circular avatar badge (28px diameter).
- **Light:** `bg=#FFFFFF`, `border: 1px solid #E7DFD7`, `text=#2A2325`, `rounded-2xl rounded-tl-sm`.
- **Dark:** `bg=#1F191C`, `border: 1px solid #382F34`, `text=#F5ECEF`, `rounded-2xl rounded-tl-sm`.
- Padding: `px-4 py-3`.
- Content: line-height 1.6, paragraphs separated by `margin-bottom: 16px`, lists indented with soft accent-colored bullets, code blocks in inset boxes (see Section 5.4).

#### Message Action Bar (below assistant bubble)
Small, subtle ghost icon bar appearing on bubble hover:
- Icons: Copy, Share, Read Aloud, Regenerate, 👍, 👎.
- Size: 16px icons, `h-7 w-7` button tap area, `rounded-lg`, color `var(--text-muted)`.
- Hover: color shifts to `var(--accent-500)`, bg `var(--accent-50)/60`.
- Transition: `opacity 150ms ease-out` (hidden by default, visible on bubble hover or focus-within).

---

### 5.4 Code Blocks

Code blocks appear as a distinct, inset container inside assistant messages:

```
+--------------------------------------------------+
| javascript                             [ Copy ]  |
|--------------------------------------------------|
| const greeting = "Hello from MEENA";             |
| console.log(greeting);                            |
+--------------------------------------------------+
```

- **Background:** `#1A1218` (both light and dark themes — consistent dark surface for code legibility).
- **Border:** `1px solid #382F34`.
- **Border Radius:** `rounded-lg` (8px).
- **Font:** `JetBrains Mono`, 13.5px, line-height 1.6.
- **Padding:** `px-4 py-3`.
- **Language label:** top-left, `var(--text-muted)`, `Micro` type style (11px, uppercase).
- **Copy button:** top-right, ghost style, fades to `var(--accent-400)` on hover.
- **Syntax highlighting:** Shiki with `catppuccin-mocha` theme (dark, warm-toned, non-neon).

---

### 5.5 Cards & Modals

#### Cards
- Background: `var(--bg-surface)`.
- Border: `1px solid var(--border-subtle)`.
- Border radius: `rounded-2xl`.
- Shadow: `var(--shadow-ambient)`.
- Padding: `p-6` (desktop), `p-4` (mobile).
- **Never stack multiple shadows. Never add inner glow effects.**

#### Modals / Dialogs (Radix UI Dialog)
- Backdrop: `backdrop-blur-sm bg-black/30` — frosted overlay, not solid black.
- Container: `max-w-lg w-full`, `rounded-2xl`, `p-6`, `var(--bg-surface)`, `var(--shadow-hover)`.
- Close button: top-right, ghost `×` icon, `h-8 w-8 rounded-lg`.
- Entry animation: `scale-95 → scale-100`, `opacity-0 → opacity-100`, `200ms cubic-bezier(0.16, 1, 0.3, 1)`.
- Exit: reverse of entry.

#### Toasts / Notifications
- Position: bottom-right, `z-50`.
- Shape: `rounded-xl`, `px-4 py-3`, `var(--bg-surface)`, `var(--shadow-hover)`, `border-l-4 border-var(--accent-500)`.
- Entry: slide up `translateY(8px) → 0`, `opacity-0 → 1`, `200ms ease-out`.
- Auto-dismiss after 4 seconds.

---

### 5.6 Sidebar

#### Structure
```
+--Sidebar (280px desktop / full mobile)--+
|  [≡]  MEENA                 [+]         |  ← Logo + Toggle + New Chat
|  [🔍 Search Chats]                      |
|─────────────────────────────────────────|
|  PINNED                                  |  ← Section label: Micro type, uppercase, text-muted
|  > Project Planning              [⋮]    |
|─────────────────────────────────────────|
|  TODAY                                   |
|  > Weekly Review Call            [⋮]    |
|  > Resume Draft                  [⋮]    |
|  YESTERDAY                               |
|  > Book Recommendations          [⋮]    |
|─────────────────────────────────────────|
|  [Avatar] Ananya Kola           [⚙]     |  ← User bar
+─────────────────────────────────────────+
```

- Sidebar background: `var(--bg-subdued)`.
- Section labels: `Micro` type, uppercase, `var(--text-muted)`, `px-4 pb-1`.
- Conversation items: `h-9`, `px-3`, `rounded-lg`, `text-sm`, truncate with ellipsis.
  - Default: `var(--text-secondary)`.
  - Active: `bg=var(--accent-50)` (light) / `bg=var(--accent-500)/15` (dark), `text=var(--accent-600)` (light) / `var(--accent-300)` (dark).
  - Hover: `bg=var(--bg-surface)` (light) / `bg=var(--bg-subdued)` (dark).
- Three-dot context menu (⋮): appears on item hover, ghost icon button `h-6 w-6 rounded-md`.

---

### 5.7 Iconography

- **Library:** `Lucide React` exclusively.
- **Stroke Width:** `1.5px` standard. `1.75px` for active/selected states. Never use `2px+` or filled shapes.
- **Sizing:** 16px for inline actions, 18px for toolbar icons, 20px for sidebar icons, 24px for feature icons.
- **Color:** `currentColor` (inherits parent). Inactive: `var(--text-muted)`. Hover: `var(--text-secondary)`. Active/selected: `var(--accent-500)`.
- **Never mix icon libraries** — no Font Awesome, no Heroicons, no Bootstrap Icons alongside Lucide.

---

## 6. Motion & Micro-Interactions

MEENA's animations must feel like natural, mindful breathing — calm and imperceptible rather than demonstrative.

### 6.1 Duration Standards

| Interaction Type | Duration | Easing |
| :--- | :--- | :--- |
| Hover color / opacity shifts | 150ms | `ease-out` |
| Button scale on press | 100ms | `ease-out` |
| Dropdown / tooltip appear | 150ms | `ease-out` |
| Dialog / drawer slide | 200ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| Sidebar collapse / expand | 250ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| Toast slide-in | 200ms | `ease-out` |
| Page transition (fade) | 150ms | `ease-in-out` |

### 6.2 Streaming Cursor Indicator

A single, soft blinking cursor rendered as a `1px × 16px` bar, `var(--accent-400)` color:
```css
@keyframes meena-blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0; }
}
.streaming-cursor {
  animation: meena-blink 1s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

Alternatively: a soft 6px × 6px dot with `animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite`.

### 6.3 Recording State (Voice Input)

A pulsing rose dot `●` with `animation: pulse 1.2s ease-in-out infinite` and a live timer `00:00` counter. The dot must clearly communicate recording without being alarming.

### 6.4 Loading Skeletons

Use skeleton placeholders (not spinners) for content areas that are loading:
- Skeleton color: `var(--border-subtle)` with a shimmer wave animation.
- Match the skeleton shape to the eventual content (text lines, avatar circles, card blocks).
- Remove skeleton immediately when real content arrives — no crossfade flash.

### 6.5 Prohibitions

- ❌ No 3D card tilt / perspective effects.
- ❌ No continuous rotating gradient borders.
- ❌ No sliding page wipes or hero parallax.
- ❌ No infinite idle animations when nothing is happening.
- ✅ Honor `prefers-reduced-motion: reduce` unconditionally — replace all positional transforms with simple `opacity` transitions.

---

## 7. Navigation & Application Shell

### 7.1 Three-Panel Layout (Desktop)

```
+───────────────────────────────────────────────────────────────────────+
│  Sidebar (280px)   │  Header (full width, 56px)                       │
│                    ├──────────────────────────────────────────────────│
│  Logo + Toggle     │  [Conversation Title ✎]   [Share] [⊘] [Options] │
│  New Chat          ├──────────────────────────────────────────────────│
│  Search            │                                                  │
│  ─────────         │         Chat Canvas (max-width: 768px,           │
│  PINNED            │                     centered, px-4)              │
│  ─────────         │                                                  │
│  TODAY             │   [MEENA avatar]  Assistant message bubble       │
│  > Chat 1          │                                                  │
│  > Chat 2          │          User message bubble (right-aligned)     │
│  YESTERDAY         │                                                  │
│  > Chat 3          │   [MEENA avatar]  Assistant message bubble       │
│                    │                                                  │
│                    ├──────────────────────────────────────────────────│
│  [Avatar] Name [⚙] │  [(+)]  Message MEENA...           [(Mic)] [↑]  │
+────────────────────┴──────────────────────────────────────────────────+
```

### 7.2 Collapsed Sidebar State (Icon Rail, Desktop)

- Width: 64px.
- Shows: MEENA logomark only, New Chat icon, Search icon, User avatar.
- Tooltips on hover for each icon.
- Chat canvas expands to fill the freed space.
- Toggle with `Ctrl/Cmd + B` or the hamburger icon.

### 7.3 Account Menu (Bottom of Sidebar)

Clicking the user avatar / name area opens a Radix Popover above the sidebar footer:

```
┌─────────────────────────────────┐
│  Ananya Kola                    │
│  ananya@example.com             │
├─────────────────────────────────│
│  👤  My Profile                 │
│  ⚙   Settings                  │
├─────────────────────────────────│
│  ➕  Add Account                │
│  ⇄   Switch Account             │
├─────────────────────────────────│
│  ✦   Upgrade Plan               │
├─────────────────────────────────│
│  ↩   Log Out                    │
└─────────────────────────────────┘
```

Style: `rounded-xl`, `var(--bg-surface)`, `var(--shadow-hover)`, `border var(--border-subtle)`, item rows `px-3 py-2 rounded-lg`, hover `var(--bg-subdued)`.

---

## 8. Responsive & Cross-Device Guidelines

### 8.1 Mobile (< 640px)
- Sidebar folds completely into a **left-sliding full-width drawer** with an accessible close button (`Esc` and tap-outside to close).
- Header: simplified — MEENA logomark, active conversation title (truncated), theme toggle, hamburger.
- Chat composer: fixed above `env(safe-area-inset-bottom)` using `padding-bottom: env(safe-area-inset-bottom)`.
- All tap targets: minimum `44 × 44px`.
- Font size base: 15px default (matches desktop default for readability).
- No hover-only interactions; all actions accessible by tap.

### 8.2 Tablet / Small Laptop (640px – 1024px)
- Sidebar toggleable via hamburger button; overlay mode (not persistent).
- Chat canvas: centered with `px-4` gutters.
- Settings: single-column layout with section tabs at top instead of left-nav.

### 8.3 Desktop (1024px+)
- Persistent multi-column layout: sidebar + main canvas.
- Settings: two-column layout (left nav + right content panel).
- Sidebar is always visible; can be collapsed to icon rail.

---

## 9. Settings Page Visual Structure

The Settings page uses a two-column layout on desktop and a tabbed/stacked layout on mobile.

```
LEFT NAV (200px)              RIGHT CONTENT PANEL
─────────────────             ───────────────────────────────────────
 Appearance                    ## Appearance
 Accent Colors                 Theme: [ Light ] [ Dark ] [ System ]
 Typography
 ─────────────                 Accent Color:
 General                       ● Pink  ○ Lavender  ○ Blue  ○ Green
 Intelligence                  ○ Peach ○ Grey      ○ Custom [#____]
 Voice
 Language                      Font:
 Notifications                 ● Plus Jakarta Sans  ○ Inter  ○ System
 ─────────────
 Personalization               Font Size:
 Memory                        ○ Small  ● Default  ○ Large
 Custom Instructions
 ─────────────
 Account & Profile
 Login & Security
 Subscription & Usage
 Storage
 ─────────────
 Privacy Center
 History & Data
 Ads Control
 ─────────────
 About MEENA
 ─────────────
 ⬤ Log Out
```

---

## 10. MEENA Brand Assets

### 10.1 Logomark
- A minimal wordmark or symbol in the brand rose accent.
- Should be legible at 16px and scale cleanly to 48px.
- Light mode: `var(--accent-500)` on `var(--bg-base)`.
- Dark mode: `var(--accent-400)` on `var(--bg-base)`.
- No drop shadows, glows, gradients, or 3D bevels on the logo.

### 10.2 Favicon & App Icon
- 32×32 favicon: simplified logomark or letter "M" in rose on a soft linen background.
- 180×180 Apple touch icon: same, padded with safe zone.
- SVG favicon preferred for crispness at all sizes.

### 10.3 Avatar / Identity Badge (MEENA)
- A 28–36px circular badge used in the chat message list preceding each assistant reply.
- Design: subtle letter "M" or logomark on `var(--accent-100)` background (light) / `var(--accent-500)/20` (dark).
- Never an anime character, robot face, or generic AI orb.

### 10.4 Empty State Illustration
- Simple, single-color SVG line illustration.
- Warm tone, hand-drawn quality, not stock vector.
- Light: `var(--text-muted)` lines on `var(--bg-base)`.
- Suggested concepts: an open notebook, a gentle leaf, a minimal speech bubble.
- Text below: *"Start a conversation — MEENA is here to listen."*

### 10.5 Loading Indicator
- Not a spinner. Use the streaming cursor (blinking vertical bar) or a soft three-dot pulse.
- Three-dot pulse: dots `6px`, color `var(--accent-400)`, `animation-delay: 0ms, 150ms, 300ms`.

---

## 11. Aesthetic Dos and Don'ts

| ✅ Do This | ❌ Avoid This |
| :--- | :--- |
| Use soft blush rose `#DF7B93` as the primary accent | Don't use hot electric neon magenta `#FF007F` |
| Use warm alabaster linen `#FAF7F2` as the page background | Don't use blinding pure `#FFFFFF` as the base background |
| Use deep velvet espresso `#161214` as the dark base | Don't use cold pitch black `#000000` or steel blue-gray dark |
| Use 1px quiet borders `#E7DFD7` to define structure | Don't use thick borders or glowing neon edge outlines |
| Give every section and message generous breathing room | Don't pack messages together in dense, airless chat logs |
| Keep all iconography at 1.5px stroke (Lucide only) | Don't mix icon libraries or use filled / 3D icon styles |
| Animate only when it aids comprehension or feedback | Don't animate idle states, decorations, or backgrounds |
| Use Shiki `catppuccin-mocha` for code highlighting | Don't use jarring bright-green-on-black terminal aesthetics |
| Support `prefers-reduced-motion` unconditionally | Don't skip the reduced motion check to "look better" |
| Respect user accent color choice throughout the app | Don't hardcode rose where the user has selected lavender |
| Mark Coming Soon features clearly with a disabled state | Don't wire up non-functional controls without explanation |
| Use muted pastel semantic colors (sage, ochre, terracotta) | Don't use pure red, green, yellow for status indicators |
