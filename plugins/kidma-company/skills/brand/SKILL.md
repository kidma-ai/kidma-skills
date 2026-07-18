---
description: "Applies Kidma's official brand colors and typography to any artifact, document, presentation, or visual output related to Kidma. Use it when brand colors, fonts, style guidelines, or visual formatting for Kidma materials apply. Covers all output types: HTML artifacts, .pptx slides, .docx documents, SVG graphics, and React components. Always use together with the relevant output-type skill (docx, pptx, etc.)."
type: reference
depends_on: []
invokes: []
---

# Kidma Brand Styling

## Overview

This skill defines Kidma's official visual identity and must be applied to **all** Kidma-branded outputs — documents, presentations, web artifacts, graphics, and UI components.

**Keywords**: Kidma branding, קידמה, corporate identity, visual identity, styling, brand colors, typography, Kidma brand, visual formatting, visual design, EdTech brand, kid-ma.com

---

## Brand Guidelines

### Colors

| Role                        | Hex       | Name          | Usage                                               |
|-----------------------------|-----------|---------------|-----------------------------------------------------|
| Primary / Background        | `#292920` | Black         | Dark backgrounds, primary text on light surfaces    |
| Background / Text           | `#F3F3F3` | White         | Light backgrounds, text on dark surfaces            |
| Accent — Light Green        | `#93DC88` | Light Green   | Accents, highlights, growth/experimentation         |
| Accent — Green              | `#61C853` | Green         | Secondary accents, buttons, a slightly bolder green |
| Accent — Blue               | `#2669F6` | Blue          | Accents, interactive/links, highlights              |
| Accent — Pink               | `#FF70A3` | Pink          | Primary CTA, highlights, creativity                 |

**Extended palette (web / marketing surfaces):**

| Role                 | Hex       | Name        | Usage                                                          |
|----------------------|-----------|-------------|----------------------------------------------------------------|
| Accent — Dark Green  | `#237520` | Dark Green  | Deep green accents, high-contrast green text                   |
| Accent — Dark Pink   | `#C42E72` | Dark Pink   | Deep pink accents, pink text on light backgrounds              |
| Accent — Coral       | `#FF9B6A` | Coral       | Warm accent; pairs with Pink in the signature gradient         |
| Surface tint         | `#FEF2F7` | Surface     | Soft pink-tinted near-white background (alt. to flat `#F3F3F3`) |

### The Three-Word Slogan & Accent Colors

Kidma's signature slogan is **"מבינים. מנסים. יוצרים."** (Understand. Try. Create.) — always written with period separators between words, and treated as a core brand asset, not just a tagline.

The three accent colors (Blue, Green, Pink) are used **decoratively** to color the slogan and other triads. There is **no fixed word→color mapping** — Kidma's own surfaces rotate the colors freely (e.g. the website's home and about pages color the three words differently). Pick whatever gives the best visual balance and contrast; just keep the colors from the brand palette.

### Color Usage Rules

- **Main palette** is Light Green, Green, Blue, and Pink.
- **Accent colors are decorative, not semantic** — there is no fixed content→color mapping. Use them for balance and emphasis.
- **CTAs:** Pink (`#FF70A3`) is the primary CTA color. Blue (`#2669F6`) or Light Green (`#93DC88`) are used as secondary CTAs depending on context — choose whichever provides better contrast and visual balance.
- **Buttons / secondary UI:** Use Green (`#61C853`) for secondary buttons and accents when you need a slightly bolder green.
- **Rotation:** When highlighting multiple distinct elements, rotate through Light Green → Blue → Pink.
- **Never use more than 3 accent colors** in a single visual element or section.

### Gradients (web / marketing)

Kidma's web and marketing surfaces lean on gradients (documents and slides stay on flat brand colors).

- **Signature gradient (primary):** Pink → Coral — `linear-gradient(135deg, #FF70A3, #FF9B6A)`. Used for hero emphasis, primary CTAs, and gradient text (`.text-gradient`).
- **Section accent gradients:** each section keys off one accent family — Blue for pedagogy, Green for technology, Pink for general/home. Fade the accent into the light background with low-opacity glows/blurs rather than hard fills.
- Keep gradients subtle and reserved for emphasis; never apply a gradient to the logo.

---

### Typography

**Primary Typeface: Assistant** — Used across *all* Kidma communications and materials. Specifically designed for Hebrew, excellent readability with a modern, technological aesthetic.

**Secondary Typeface: Rubik** — Complements Assistant for special elements, emphasis, and materials targeting younger audiences. Not a body text replacement.

#### Full Typographic Hierarchy

| Level                | Font                 | Weight | Size (digital) | Size (print) | Line Height | Letter Spacing | Alignment  |
|----------------------|----------------------|--------|----------------|--------------|-------------|----------------|------------|
| H1 — Primary Headline| Assistant Black      | 900    | 32px           | 28pt         | 120%        | −1% (tight)    | Right (RTL)|
| H2 — Secondary Headline | Assistant Bold    | 700    | 24px           | 20pt         | 130%        | 0%             | Right (RTL)|
| H3 — Tertiary Headline  | Assistant SemiBold| 600    | 20px           | 16pt         | 140%        | 0%             | Right (RTL)|
| Body Text            | Assistant Regular    | 400    | 16px           | 11pt         | 160%        | 0%             | Right (RTL)|
| Small / Captions     | Assistant Light      | 300    | 14px           | 9pt          | 150%        | 0%             | Right (RTL)|
| Menus / Buttons / UI | Assistant Medium     | 500    | 16px           | —            | —           | 0%             | —          |
| Special / Emphasis   | Rubik Bold           | 700    | As needed      | —            | —           | —              | —          |
| Special / Secondary  | Rubik Medium/Regular | 400–500| As needed      | —            | —           | —              | —          |

#### Typography Rules

- **Assistant is the primary font for ALL text** — headlines, body, captions, UI labels.
- **Rubik is secondary only** — use for special design elements, call-outs, or materials specifically targeting younger students.
- Never use text smaller than **14px** in digital materials.
- Maintain minimum contrast ratio of **4.5:1** between text and background.
- Use **RTL alignment** for all Hebrew text.
- Accent colors applied to type are **decorative** — there is no fixed word→color mapping.

---

### Appearances

Kidma has two appearance modes. **Light is the default.** The only thing that changes between modes is the background color — all other colors (text, accents, fonts) remain identical.

| Mode                | Background  | Text / Foreground |
|---------------------|-------------|-------------------|
| **Light (default)** | `#F3F3F3`   | `#292920`         |
| **Dark**            | `#292920`   | `#F3F3F3`         |

> **Rule:** Always use Light mode unless the user explicitly requests Dark mode or the output context calls for it (e.g., a slide title page, a dark-themed screen UI).

---

### Layout & Visual Principles

- **Accent as a highlight tool:** Use accent colors sparingly for borders, badges, underlines, icons, and highlights — not as solid fills for large areas.
- **High contrast:** All text must meet WCAG AA contrast ratio minimums against its background.
- **RTL support:** Kidma materials are often in Hebrew. Always configure RTL (`direction: rtl`, `text-align: right`) when producing Hebrew content.
- **Clean & minimal:** Avoid decorative clutter. Whitespace is intentional. Prefer bold typography over complex graphic elements.
- **Consistent margins (print):** Minimum 10mm on all sides.

---

## Logo

### Logo Variants

There are **4 logo files**, covering 2 modes × 2 layouts:

| File | Mode | Layout | Use when |
|------|------|--------|----------|
| `logo_b_top.png`  | **Light** (black logo) | Stacked (icon above text) | **Default** — top of page, header, center placement on light backgrounds |
| `logo_b_side.png` | **Light** (black logo) | Horizontal (icon beside text) | Logo is placed in a sidebar or along the side of a document/screen on light backgrounds |
| `logo_w_top.png`  | **Dark** (white logo)  | Stacked (icon above text) | **Default dark** — top of page, header, center placement on dark backgrounds |
| `logo_w_side.png` | **Dark** (white logo)  | Horizontal (icon beside text) | Logo is placed in a sidebar or along the side of a document/screen on dark backgrounds |

**All files are stored at:** `${CLAUDE_PLUGIN_ROOT}/assets/`

### Selecting the Right Logo

```
Light mode background (#F3F3F3)?
  → Top / header / center placement  → logo_b_top.png  ← DEFAULT
  → Sidebar / side of screen         → logo_b_side.png

Dark mode background (#292920)?
  → Top / header / center placement  → logo_w_top.png  ← DEFAULT DARK
  → Sidebar / side of screen         → logo_w_side.png
```

### Usage Guidelines
- The Kidma logo should appear on all external-facing artifacts (presentations, documents, web pages).
- Place the logo in the **top-right corner** for RTL (Hebrew) layouts, or **top-left corner** for LTR layouts.
- Minimum clear space: the height of the letter "ק" on all sides.
- Minimum size: 30px height for digital, 15mm for print.
- Never stretch, recolor, add shadows, gradients, or other effects to the logo.
- Always match the logo variant to the background mode — never place a black logo on a dark background or a white logo on a light background.

### Code Snippets

**HTML/React (light mode, default):**
```html
<img src="${CLAUDE_PLUGIN_ROOT}/assets/logo_b_top.png" alt="Kidma" style="height: 60px;" />
```

**python-pptx (.pptx):**
```python
from pptx.util import Inches

LOGO_DIR = "${CLAUDE_PLUGIN_ROOT}/assets/"

# Pick the right logo based on slide background and placement
logo_file = LOGO_DIR + "logo_b_top.png"   # light bg, top/center → DEFAULT
# logo_file = LOGO_DIR + "logo_b_side.png" # light bg, sidebar
# logo_file = LOGO_DIR + "logo_w_top.png"  # dark bg, top/center
# logo_file = LOGO_DIR + "logo_w_side.png" # dark bg, sidebar

slide.shapes.add_picture(
    logo_file,
    left=Inches(0.3), top=Inches(0.2),
    height=Inches(0.7)
)
```

**python-docx (.docx):**
```python
from docx.shared import Inches

# Documents default to light mode, top placement → black stacked logo
doc.add_picture(
    "${CLAUDE_PLUGIN_ROOT}/assets/logo_b_top.png",
    width=Inches(1.2)
)
```

---

## Output-Specific Styling

### HTML / React Artifacts

```css
/* CSS Variables — add to :root */
:root {
  --kidma-black:        #292920;
  --kidma-white:        #F3F3F3;
  --kidma-green-light:  #93DC88;  /* light green accent */
  --kidma-green-dark:   #61C853;  /* green — secondary accents / buttons */
  --kidma-blue:         #2669F6;  /* blue accent */
  --kidma-pink:         #FF70A3;  /* pink — primary CTA */
  /* Extended palette (web / marketing) */
  --kidma-green-deep:   #237520;  /* dark green (site token: --color-kidma-green-dark) */
  --kidma-pink-deep:    #C42E72;  /* dark pink (site token: --color-kidma-pink-dark) */
  --kidma-coral:        #FF9B6A;  /* coral — pairs with pink in the signature gradient */
  --kidma-surface:      #FEF2F7;  /* soft pink-tinted near-white background */
  --kidma-gradient:     linear-gradient(135deg, #FF70A3, #FF9B6A);  /* signature pink→coral */
  --font-primary:  'Assistant', Arial, sans-serif;
  --font-secondary: 'Rubik', sans-serif;
}

/* Light mode (default) */
body {
  background-color: var(--kidma-white);
  color: var(--kidma-black);
  font-family: var(--font-primary);
  font-size: 16px;
  line-height: 1.6;
}

/* Dark mode — apply .kidma-dark to <body> or a wrapper */
body.kidma-dark {
  background-color: var(--kidma-black);
  color: var(--kidma-white);
}

h1 { font-family: var(--font-primary); font-weight: 900; font-size: 32px; line-height: 1.2; letter-spacing: -0.01em; }
h2 { font-family: var(--font-primary); font-weight: 700; font-size: 24px; line-height: 1.3; }
h3 { font-family: var(--font-primary); font-weight: 600; font-size: 20px; line-height: 1.4; }
p, li, td { font-family: var(--font-primary); font-weight: 400; font-size: 16px; line-height: 1.6; }
small, caption { font-family: var(--font-primary); font-weight: 300; font-size: 14px; line-height: 1.5; }
button, .label { font-family: var(--font-primary); font-weight: 500; }

/* Special / emphasis elements only */
.special-element { font-family: var(--font-secondary); }
```

Load fonts from Google Fonts when building HTML artifacts:
```html
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;500;600;700;900&family=Rubik:wght@400;500;700&display=swap" rel="stylesheet">
```

---

### PowerPoint (.pptx)

- **Slide background:** `#F3F3F3` (light, default) for most slides; `#292920` (dark) for title/section slides or when dark mode is requested.
- **Title text:** `Assistant Black (900)` or `Assistant Bold (700)`, `#292920` on light slides; `#F3F3F3` on dark slides.
- **Body text:** `Assistant Regular (400)`, same color logic as titles.
- **Accent shapes / lines:** Rotate the accent palette (Light Green → Blue → Pink) for balance — the colors are decorative, not semantic.
- **RGB values for python-pptx:**

```python
from pptx.util import Pt
from pptx.dml.color import RGBColor

KIDMA_BLACK        = RGBColor(0x29, 0x29, 0x20)
KIDMA_WHITE        = RGBColor(0xF3, 0xF3, 0xF3)
KIDMA_GREEN_LIGHT  = RGBColor(0x93, 0xDC, 0x88)  # light green accent
KIDMA_GREEN_DARK   = RGBColor(0x61, 0xC8, 0x53)  # green — secondary accents / buttons
KIDMA_BLUE         = RGBColor(0x26, 0x69, 0xF6)  # blue accent
KIDMA_PINK         = RGBColor(0xFF, 0x70, 0xA3)  # pink — primary CTA
```

---

### Word Documents (.docx)

- **Heading styles:** `Assistant` (Black 900 / Bold 700 / SemiBold 600 depending on level), `#292920`.
- **Body styles:** `Assistant Regular (400)`, `#292920` on white page background.
- **Accent elements** (borders, table headers, callout boxes, highlights): Rotate the accent palette (Light Green → Blue → Pink) for balance — decorative, not semantic.
- **Page background:** White (`#FFFFFF`) — `.docx` documents default to light mode.
- **RTL:** Set section direction to RTL for Hebrew documents.
- For branded Kidma `.docx` files, also read the `kidma-lesson-docx` skill for the official wave-design template.

---

### SVG Graphics

```svg
<!-- Kidma SVG palette reference -->
<defs>
  <style>
    .k-bg          { fill: #292920; }
    .k-light       { fill: #F3F3F3; }
    .k-green-light { fill: #93DC88; } /* light green accent */
    .k-green-dark  { fill: #61C853; } /* green — secondary accents */
    .k-blue        { fill: #2669F6; } /* blue accent */
    .k-pink        { fill: #FF70A3; } /* pink — primary CTA */
  </style>
</defs>
```

---

## Quick Checklist

Before delivering any Kidma-branded output, verify:

- [ ] Background is `#F3F3F3` (light mode, default) or `#292920` (dark mode, when explicitly requested)
- [ ] Headlines use `Assistant` (Black 900 / Bold 700 / SemiBold 600 by level)
- [ ] Body text uses `Assistant Regular (400)` — **not Rubik**
- [ ] Rubik used only for special/emphasis elements, not general body text
- [ ] At least one accent color from the palette is present
- [ ] Accent colors used decoratively for balance (no fixed word→color mapping required)
- [ ] No more than 3 accent colors used in the same visual
- [ ] Hebrew content is RTL-configured
- [ ] Text contrast is legible (minimum 4.5:1 ratio)
- [ ] Text is never smaller than 14px in digital materials
- [ ] Kidma logo or name is present if this is an external-facing artifact

---

## Related Skills

- **`kidma-plugins:overview`** — Full company context, programs, and business information
- **`kidma-plugins:lesson-to-word`** — Branded Word document template with wave design
- **`kidma-plugins:slides-builder`** — Branded PowerPoint file generation
- **`kidma-plugins:slides-planner`** — Slide content planning for Kidma lessons
- **`kidma-plugins:lesson-planner`** — Lesson plan content following Kidma pedagogy
