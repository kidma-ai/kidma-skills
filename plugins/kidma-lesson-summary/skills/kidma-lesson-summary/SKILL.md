---
description: "Generate a branded 1-2 page Kidma lesson summary PDF for students. The summary distills the core concepts, key terms, processes, and takeaways from a lesson so that any student who missed the class can catch up quickly. Content is sourced from the lesson's slides (kidma-presentation-builder) and/or the instructor lesson plan doc (kidma-lesson-docx). Style follows Kidma brand guidelines exactly (Assistant font, brand colors, wave footer, RTL Hebrew). Output is a ready-to-distribute PDF file. Use this skill when the user asks to: - Create a \"סיכום שיעור\" (lesson summary) PDF - Generate a student handout / take-home sheet for a lesson - Build a catch-up document for absent students - Produce a reference card summarizing a Kidma lesson - Says anything like \"תן לי סיכום לשיעור\", \"צור דף סיכום\", \"סיכום לתלמיד\",    \"student summary\", \"lesson recap PDF\", \"דף מסכם לתלמיד\""
---

# Kidma Lesson Summary PDF — Skill

## Purpose

This skill produces a **1-2 page branded PDF** that summarizes a single Kidma lesson.
The document is written for **students**, not instructors — it uses clear, concise Hebrew,
covers key concepts, vocabulary, processes, and a closing tip or takeaway.

Think of it as: *"Everything a student needs to understand the lesson if they weren't there."*

---

## Prerequisites — Read These First

Before generating any summary, always also read:
- `kidma-plugins:kidma-brand-guidelines skill` — colors, fonts, logos
- `the pdf public skill` — PDF creation tooling (WeasyPrint approach)

---

## Content Sources

The summary content can come from **any combination** of these sources:

| Source | What to extract |
|--------|-----------------|
| **Lesson slides** (`.pptx` or slide plan from `kidma-presentation-planner`) | Key concepts per slide, vocabulary terms, diagrams described in text |
| **Instructor lesson plan** (`.docx` from `kidma-lesson-docx` or Google Doc) | Phase content, theory explanations, analogy text, learning objectives |
| **Lesson summary files** uploaded by user | Direct extraction from provided PDFs/docs |
| **Conversation context** | If the user pastes or describes the lesson content directly |

**Priority rule:** Always prefer the slides for the "Understanding" content (what was shown to students), and the instructor doc for deeper explanations of concepts.

---

## What to Include in the Summary (Content Rules)

### ✅ Always include:
1. **מושגי יסוד (Core Vocabulary)** — All new terms defined in the lesson, with the English name and a 1-sentence Hebrew explanation
2. **מסרים מרכזיים (Key Concepts)** — The 2-4 main ideas of the lesson in plain language
3. **תהליכים / שלבים (Processes / Steps)** — Any numbered process (e.g., how diffusion works, how AI translates text) — use numbered list format
4. **טיפים מרכזיים (Key Tips)** — Practical tips for students (prompt writing tips, translation tips, etc.)
5. **💡 זכרו (Remember / Callout)** — A closing highlight box with the single most important takeaway

### ❌ Never include:
- Instructor-facing notes or classroom management tips
- Technical implementation details beyond student level
- Content from the Assessment or Materials sections of the lesson plan
- Anything longer than 2 pages — if content is too long, prioritize vocabulary + key concepts + process, and trim tips

---

## Section Design System

Each content block in the summary uses a **colored section header** that maps to Kidma's methodology colors:

| Content Type | `"color"` value | Header BG | Bullet Color | When to use |
|---|---|---|---|---|
| Vocabulary / terms | `"vocab"` | Blue `#2669F6` | Blue | Key terms section |
| Understanding / concepts | `"understand"` | Blue `#2669F6` | Blue | Main ideas, how things work |
| Try / experimentation | `"try"` | Green `#93DC88` | Green | Tips, practice, process steps |
| Create / output | `"create"` | Pink `#FF70A3` | Pink | Creation task description |
| Process / numbered steps | `"process"` | Dark `#292920` | Dark | Step-by-step processes |
| General / other | `"default"` | Dark `#292920` | Dark | Anything not covered above |
| Callout / highlight | *(any color)* + `"type":"callout"` | Gray box | — | Single key takeaway or warning |

---

## JSON Schema

Build the summary as a JSON object following this schema:

```json
{
  "lesson_title": "סיכום שיעור [שם השיעור]",
  "lesson_subtitle": "תת-כותרת (נושאי המשנה של השיעור)",
  "two_column": false,
  "sections": [
    {
      "title": "כותרת הסקשן בעברית",
      "color": "vocab",
      "type": "bullets",
      "items": [
        {
          "term": "מונח בעברית – English Term",
          "text": "הגדרה קצרה וברורה של המונח."
        }
      ]
    },
    {
      "title": "תהליך / שלבים",
      "color": "process",
      "type": "steps",
      "items": [
        { "term": "שלב 1 — ניתוח טקסט", "text": "הבינה מבינה מה הטקסט מבקש." },
        { "term": "שלב 2 — ניתוח לשוני", "text": "לימוד אופן הביטוי הנכון של המילים." }
      ]
    },
    {
      "title": "💡 זכרו",
      "color": "default",
      "type": "callout",
      "content": "הבינה המלאכותית היא כלי חזק אך לא מושלם. תמיד בדקו ואמתו."
    }
  ]
}
```

### Field reference

| Field | Type | Description |
|---|---|---|
| `lesson_title` | string | Full title shown at top, e.g. `"סיכום שיעור טקסט לדיבור"` |
| `lesson_subtitle` | string | Subtitle/topic line shown below title |
| `two_column` | bool | `true` splits sections into a 2-column grid (good for content-heavy summaries) |
| `sections[].title` | string | Section header text |
| `sections[].color` | string | One of: `vocab`, `understand`, `try`, `create`, `process`, `tips`, `default` |
| `sections[].type` | string | `"bullets"` (default), `"steps"` (numbered), `"callout"` (highlight box), `"text"` (plain paragraph) |
| `sections[].items` | array | For `bullets` and `steps`: array of `{term?, text}` objects |
| `sections[].content` | string | For `callout` and `text` types: the paragraph/box content |
| `items[].term` | string | Optional bold label before the bullet text |
| `items[].text` | string | The bullet/step body text |

### Recommended section order

1. `מושגי יסוד` — vocabulary (color: `vocab`)
2. Main concept section(s) — how it works, what it is (color: `understand`)  
3. Process / steps if applicable (color: `process`)
4. Tips / best practices (color: `tips`)
5. `💡 זכרו` callout — single closing takeaway

---

## Generation Workflow

### Step 1 — Extract content from source materials

Read the lesson plan and/or slides. Extract:
- All new vocabulary terms with their definitions
- The core 2-4 ideas students should understand
- Any numbered processes explained in the lesson
- Key practical tips taught (prompt writing, translation tips, etc.)
- The single most important takeaway

### Step 2 — Build the JSON

Write the `summary_content.json` at `/home/claude/summary_content.json` following the schema above.

**Length check:** Before proceeding, count the bullet items across all sections. If there are more than ~25 items total across all sections, trim to the most essential — the summary must fit 1-2 pages.

### Step 3 — Run the generator script

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_summary.py \
  /home/claude/summary_content.json \
  /home/claude/lesson_summary.pdf
```

### Step 4 — Copy to output and deliver

```bash
cp /home/claude/lesson_summary.pdf /mnt/user-data/outputs/lesson_summary.pdf
```

Then call `present_files` to share with the user.

---

## Tips & Edge Cases

### If content is very short (< 1 full page)
Increase font sizes or add a "דברים שלמדנו היום" (What we learned today) recap section at the top that lists 3 bullet points summarizing the lesson at a high level.

### If content is very long (would exceed 2 pages)
1. Set `"two_column": true` to fit more content per page
2. Trim each bullet to 1 sentence maximum
3. Remove the Tips section if necessary — keep Vocabulary + Key Concepts + Process

### Hebrew font rendering
The generator embeds the **Assistant** font from Google Fonts. If offline/no network access, fall back to:
```python
# In the CSS block, replace the @import with:
# Nothing — Arial will be used as fallback, still readable
```

### If the user provides slide content as Google Slides link
Use `google_drive_fetch` or `web_fetch` to retrieve the slide content, then extract the text from each slide and map to the JSON schema.

### Two-column layout example (for content-heavy lessons)
```json
{
  "lesson_title": "סיכום שיעור חשיבה ביקורתית",
  "lesson_subtitle": "כתיבת מאמר בסיוע בינה מלאכותית",
  "two_column": true,
  "sections": [...]
}
```

---

## Example Summaries (Reference)

These are Kidma's real student summaries — use them as style reference:

| Lesson | File |
|---|---|
| מבוא לבינה מלאכותית | `/mnt/user-data/uploads/סיכום_שיעור_-_מבוא_לבינה_מלאכותית.pdf` |
| טקסט לדיבור | `/mnt/user-data/uploads/סיכום_שיעור_-_טקסט_לדיבור.pdf` |
| בדמיון – טקסט לתמונה | `/mnt/user-data/uploads/סיכום_שיעור_בדמיון_-_טקסט_לתמונה.pdf` |
| חשיבה ביקורתית | `/mnt/user-data/uploads/סיכום_שיעור_חשיבה_ביקורתית.pdf` |
| השוואה שימושית (docx) | `/mnt/user-data/uploads/סיכום_שיעור_-_השוואה_שימושית.docx` |

**Key visual patterns observed in these examples:**
- Title: large, centered, bold — `"סיכום שיעור [שם השיעור]"`
- Subtitle: smaller, gray, centered — the lesson sub-topic
- Kidma logo top-right, MoE badge top-left, separated by a green line
- Colored section headers (inline, rounded pill shape)
- Colored bullet dots matching the section header color
- Bold term + dash + explanation format for vocabulary
- Numbered steps with bold step labels for processes
- Wave gradient footer (pink → orange → green → blue)
- Maximum 2 pages, clean whitespace

---

## Script Location

```
${CLAUDE_PLUGIN_ROOT}/scripts/generate_summary.py
```

The script accepts:
```
python3 generate_summary.py <input_json> <output_pdf>
```

It automatically:
- Embeds the Kidma logo as base64 (no external file reference needed in output)
- Applies all brand colors, fonts, RTL direction
- Renders the wave footer
- Handles all section types (`bullets`, `steps`, `callout`, `text`, 2-column grid)

---

## Related Skills

- **`kidma-presentation-builder`** — Source of slide content for summaries
- **`kidma-lesson-docx`** — Source of instructor lesson plan content
- **`kidma-lesson-generator`** — Generates lesson content JSON (can be adapted for summaries)
- **`kidma-brand-guidelines`** — Brand colors, fonts, logo rules
- **`kidma-company-overview`** — Full Kidma program context