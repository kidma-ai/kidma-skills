---
description: "Plan and design the content for a Kidma lesson presentation through an interactive, user-in-the-loop workflow. ALWAYS use this skill when the user asks to create slides, a presentation, a מצגת, or a slide deck for any Kidma lesson. Also trigger when the user mentions 'make slides for lesson X', 'create a presentation for the AI music lesson', or any task involving turning Kidma lesson content into a visual presentation. This skill guides the user through outline creation, slide-by-slide content review, and approval before handing off to the slides-builder skill for file generation. Use this skill FIRST — never jump straight to building the .pptx file without going through this planning process."
type: interactive
depends_on:
  - kidma-plugins:overview
  - kidma-plugins:brand
invokes:
  - slides-builder
output_format: text
output_file: "/home/claude/presentation_plan.txt"
---

# Kidma Presentation Planner

An interactive skill that collaborates with the user to plan a high-quality Kidma lesson presentation. This skill handles **content and structure only** — once the plan is approved, it hands off to the `kidma-presentation-builder` skill for .pptx file creation.

## Why This Skill Exists

Presentation quality depends on getting the content right before touching any files. This skill ensures:
- The flow and narrative arc make sense for the specific lesson
- Each slide has a clear purpose and the right structure
- Content is precise, concise, and pedagogically sound
- The user approves everything before file generation begins

---

## Workflow Overview

```
Phase 1: Understand the Lesson → Extract content blocks
Phase 2: Propose Outline       → Present flow + get approval
Phase 3: Slide-by-Slide Review → Walk through each slide's content
Phase 4: Final Approval        → Confirm the complete plan
Phase 5: Hand Off              → Launch kidma-presentation-builder
```

---

## Phase 1: Understand the Lesson

### If a lesson plan document is provided:
Extract these content blocks from the lesson plan (מערך שיעור):

| Block | Source Section | What to Extract |
|-------|---------------|-----------------|
| **Title** | שם השיעור | Catchy title + topic subtitle |
| **Lesson number** | Header | "שיעור X" if part of a series |
| **Ice-breaker** | הקדמה phase | Opening question connected to output |
| **Agenda topics** | מבנה השיעור | 3-4 main topic names |
| **Key concepts** | הבנה phase | Technical terms (Hebrew + English) with definitions |
| **Theory content** | הבנה phase | Analogies, explanations, process descriptions |
| **Domain vocabulary** | הבנה phase | Professional terms for the AI domain |
| **Experimentation task** | התנסות phase | What everyone does together |
| **Creation task** | יצירה phase | Personal output + specific AI tools + requirements |
| **Closing question** | סיכום phase | Recap points + discussion question |

Present a brief summary to the user: "Here's what I extracted from the lesson plan — does this capture everything?"

### Gap Detection

After extraction, check for missing or unclear elements:
- **No distinct experimentation task?** Ask: "I didn't find a separate guided experimentation task — should I add one, or fold it into the creation phase?"
- **No ice-breaker?** Suggest one based on the lesson topic
- **Vague creation task?** Ask for specific tool names and deliverable details
- **Missing domain vocabulary?** Propose relevant terms from the topic area

Always flag gaps explicitly rather than silently filling them in.

### If no lesson plan is provided:
Ask the user for:
1. What is the lesson topic?
2. What program is it for? (Advanced A, Advanced B, Workshop, Or Program)
3. What AI tools will students use?
4. What should students create as their output?
5. Are there specific concepts or vocabulary to cover?

---

## Phase 2: Propose the Outline

Based on the extracted content, propose a **presentation outline** showing the full slide sequence.

### Outline Format

Present the outline as a numbered list. For each slide, show:
- **Slide number**
- **Slide type** (from the template catalog — see `references/slide-types.md`)
- **Pedagogical phase** — which lesson phase this maps to (הקדמה / הבנה / התנסות / יצירה / סיכום)
- **Purpose** — what this slide achieves in the lesson flow
- **Title** (Hebrew) — the proposed slide title
- **Key content** — 1-2 sentence summary of what goes on this slide

### Example Outline Presentation

```
📊 מצגת שיעור 6 — מוזיקה עם בינה מלאכותית

שקף 1 | כריכה (Cover) | פתיחת השיעור
  כותרת: "צלילי העתיד 🎵"
  תת-כותרת: מוזיקה עם בינה מלאכותית | שיעור 6

שקף 2 | סדר יום (Topics Overview) | מה נלמד היום
  4 נושאים: מוזיקה וטכנולוגיה, איך AI יוצר מוזיקה, אוצר מילים מוזיקלי, יצירת שיר

שקף 3 | תוכן (Content - Blue) | רקע: מוזיקה וטכנולוגיה
  הקשר היסטורי — איך טכנולוגיה שינתה מוזיקה לאורך השנים

שקף 4 | תוכן (Content - Green) | מושג מפתח: מודל מוזיקלי
  הסבר איך AI לומד ליצור מוזיקה מדוגמאות

...

שקף 11 | משימה (Task) | משימת היצירה
  4 שלבים + כלי AI לכל שלב

שקף 12 | סיכום (Summary) | מה למדנו + שאלה למחשבה
```

### Target: 10–15 slides

**Ask the user:** "Here's my proposed flow for the presentation. Does this structure work? Would you add, remove, or reorder anything?"

Wait for approval before proceeding. Iterate on the outline until the user is satisfied.

---

## Phase 3: Slide-by-Slide Review

Once the outline is approved, go through each slide and present the **full content** for that slide.

### For each slide, present:

1. **Slide type & template** — which template slide to use (reference the catalog)
2. **Title** (כותרת) — the Hebrew title
3. **Subtitle/Description** (תיאור) — if applicable
4. **Content** — the full text that will appear on the slide:
   - Bullet points (max 3 per slide)
   - Terms with definitions
   - Process steps
   - Task instructions
   - etc.
5. **Visual notes** — any specific visual elements (emojis, tool badges, color notes)

### Batching Strategy

Don't overwhelm the user with 12 slides at once. Present in logical batches:

- **Batch 1: Opening** (Cover + Agenda) — 2 slides
- **Batch 2: Theory/Concepts** (Key concepts + explanations) — 3-5 slides
- **Batch 3: Practice** (Experimentation + examples) — 2-3 slides
- **Batch 4: Creation + Closing** (Task + Summary) — 2-3 slides

After each batch, ask: "How does this batch look? Any changes needed?"

Use the `ask_user_input` tool for quick batch approvals when the content looks straightforward. For example, offer choices like "Looks good, next batch" / "I have changes" / "Let me think about it". For the outline approval in Phase 2, also use `ask_user_input` with options like "Approve outline" / "I want to add slides" / "I want to remove/change slides".

### Content Rules (enforce these during review)

- **All text in Hebrew** — technical terms bilingual: "למידת מכונה (Machine Learning)"
- **Max 3 bullet points** per content slide — slides are visual aids, not textbooks
- **Concise language** — each bullet should be 1-2 lines max
- **Use emojis** where appropriate: 📖 💬 🤖 ✨ 🎨 ❌ ✅ 💡 🎯 🤔
- **Tool names** must be specific on task slides (not "AI tool" but "Gemini", "DALL·E", etc.)
- **Warm, student-friendly tone** — age-appropriate language, everyday metaphors

---

## Phase 4: Final Approval

Once all slides are reviewed, present a **complete summary** of the final plan:

```
✅ סיכום המצגת — [Lesson Title]

📊 סה"כ שקפים: [N]
🎯 קהל יעד: [program type]
⏱️ זמן שיעור: 90 דקות

רשימת שקפים:
1. [Title] — [slide type]
2. [Title] — [slide type]
...

מוכנים ליצור את הקובץ?
```

**Ask:** "This is the final plan. Should I go ahead and create the presentation file?"

---

## Phase 5: Hand Off to Builder

Once the user confirms, instruct Claude to:

1. Read the `slides-builder` skill: `kidma-plugins:slides-builder skill`
2. Pass the complete approved plan (all slide content, types, and sequence)
3. The builder skill handles all .pptx file creation

**Important:** Write out the full approved plan in a structured format that the builder can consume directly. Use this format:

```
=== APPROVED PRESENTATION PLAN ===

METADATA:
- Title: [lesson title]
- Subtitle: [subtitle]
- Lesson Number: [N or "standalone"]
- Total Slides: [N]

SLIDES:

[Slide 1]
- Template: Slide 2 (Cover)
- Title: [Hebrew title]
- Subtitle: [subtitle]
- Description: [description]
- Lesson Number: [שיעור X]

[Slide 2]
- Template: Slide 13 (Topics Overview)
- Topics:
  1. [topic 1]
  2. [topic 2]
  3. [topic 3]
  4. [topic 4]

[Slide 3]
- Template: Slide [N] ([type], [color])
- Title: [Hebrew title]
- Description: [description]
- Content Label: [label]
- Bullet 1: [text]
- Bullet 2: [text]
- Bullet 3: [text]

... (continue for all slides)

=== END PLAN ===
```

---

## Reference Files

Read `references/slide-types.md` when you need:
- Quick reference of all available template slide types
- Which slide type works for which content
- Layout constraints and placeholder counts

Read `references/summary-patterns.md` when you also need to create a post-lesson student summary (סיכום שיעור) — this is a separate deliverable from the presentation.
