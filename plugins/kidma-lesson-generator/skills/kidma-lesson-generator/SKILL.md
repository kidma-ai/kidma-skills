---
description: "Generate Kidma-style lesson plan CONTENT (מערכי שיעור) that follows Kidma's proprietary pedagogical structure and patterns. Use this skill whenever the user asks to create, write, draft, or design a new Kidma lesson plan, teaching session, student task sheet, workshop plan, or curriculum unit — whether for students or teachers. Also trigger when the user wants to adapt an existing topic into Kidma's format, asks about Kidma lesson structure or pedagogy, wants to generate instructor guides or student task sheets, or says anything like 'write a lesson about X for Kidma', 'create a new session for Advanced A/B', 'make a workshop plan', or 'generate a מערך שיעור'. This skill generates the CONTENT ONLY — it outputs a structured JSON file that can then be fed into the kidma-lesson-docx skill for formatting. If the user also wants the final .docx file, use this skill first to generate content, then use kidma-lesson-docx to produce the formatted document."
---

# Kidma Lesson Content Generator

This is a **collaborative, user-in-the-loop** skill. The core principle: **confirm the key decisions before writing the full detailed plan.** How you get there depends on how much context the user provides.

## Core Principle

Never generate the full lesson plan in one shot. There are three key decisions that must be aligned with the user before generating the detailed plan:

1. **What's the core idea?** — topic, central concept, why it matters
2. **What are the three learning stages?** — what students understand, experiment with, and create
3. **What's the student artifact?** — the exact deliverable, requirements, and how it's submitted

Once these are confirmed, generate the full detailed plan and present for final review.

## Adaptive Flow

**Read the user's input and adapt.** The phases below are guidelines, not a rigid script:

| User provides... | You should... |
|---|---|
| Just a topic ("lesson about AI music") | Walk through all phases gradually |
| Topic + some ideas ("AI music, I want them to create a song using Suno") | Propose a combined Phase 1+2+3, confirm, then generate |
| Detailed brief with topic, stages, artifact, and tools | Skip to Phase 4 — summarize what you understood, confirm, generate |
| Approval + "just go with it" | Compress remaining phases, generate, present for review |

**When in doubt, propose and ask** rather than asking open-ended questions. It's faster for the user to react to a concrete suggestion than to answer from scratch.

---

## Phase 1: Topic & Core Idea

**Goal:** Align on WHAT the lesson is about and WHY it matters.

Gather or infer from context:
- What is the topic?
- Which program? (Advanced A, Advanced B, Workshop, Or program)
- Lesson number in the sequence? (if applicable)
- Age group / grade?

**Propose** (in Hebrew):

1. **שם השיעור** — A catchy lesson title + subtitle
2. **הרעיון המרכזי** — The core AI concept being taught (1–2 sentences)
3. **למה זה חשוב** — Why this matters for students (1 sentence)

Example:
> **שם השיעור:** שיעור 6 — מוזיקה עם בינה מלאכותית
> **הרעיון המרכזי:** כיצד AI יכול ליצור מוזיקה מתוך תיאור טקסטואלי, ומהם המושגים המוזיקליים שצריך להכיר כדי ליצור פרומפט מוזיקלי טוב.
> **למה זה חשוב:** התלמידים ילמדו שגם ביצירה אמנותית כמו מוזיקה, הפרומפט הוא המלך — ככל שהתיאור מדויק יותר, התוצאה טובה יותר.

**Ask for approval** — use the ask_user_input tool when appropriate. Move on when aligned.

---

## Phase 2: Three Learning Stages

**Goal:** Define what happens in הבנה, התנסות, יצירה.

**Propose** (in Hebrew) a breakdown for each stage:

### הבנה (Understanding) — ~20 דקות
- What 3–5 concepts will students learn?
- What analogy/metaphor will make it click? (cooking, LEGO, travel, etc.)
- What domain vocabulary will be introduced? (Hebrew + English terms)
- What demo or video will anchor the theory?

### התנסות (Experimentation) — ~20 דקות
- What is the **shared task** everyone does together?
- What comparison will they make? (e.g., different prompts, changing one parameter)
- What is the specific "aha moment" you're designing for?

### יצירה (Creation) — ~35 דקות
- What is the **personal creation task**?
- What constraints or requirements make it interesting?
- How does peer collaboration happen?

**Key pedagogical principles to apply when proposing:**
- Start from the end — define the desired output first, then work backwards
- "The Prompt is King" — every stage reinforces prompt quality
- Role-Based Prompting — students assign roles to the AI
- Domain Vocabulary — include professional terms for this AI domain
- Paper First, Screen Second — especially for image/visual lessons
- Iteration is Expected — build in "improve your prompt" steps

**Ask for approval.** The user may want to adjust the balance, swap concepts, change tasks.

---

## Phase 3: Student Artifact

**Goal:** Define the exact deliverable students create and submit.

**Propose** (in Hebrew):

1. **התוצר** — What exactly will students create? (be specific: "a 30-second AI-generated song in a genre of their choice", not just "music")
2. **כלי העבודה** — Which specific AI tools are used
3. **דרישות** — 3–4 specific requirements/constraints that ensure quality
4. **הגשה** — How students submit (Kidma Portal)
5. **שאלת הפתיחה** — An engaging ice-breaker question for the intro that connects to the artifact

Example:
> **התוצר:** כל תלמיד ייצור קטע מוזיקלי אישי (30 שניות לפחות) בסגנון שבחר, באמצעות כלי יצירת המוזיקה בפורטל.
> **כלי העבודה:** כלי יצירת מוזיקה AI בפורטל קידמה
> **דרישות:**
> 1. הפרומפט חייב לכלול לפחות 4 מושגים מקצועיים
> 2. התלמיד חייב לשפר את הפרומפט לפחות פעם אחת
> 3. התלמיד יכתוב על דף נייר את הרעיון לפני הכתיבה בפורטל
> **הגשה:** פורטל קידמה
> **שאלת הפתיחה:** "מה השיר האהוב עליכם? מה גורם לשיר להיות טוב?"

**Ask for approval before generating the full plan.**

---

## Phase 4: Full Lesson Plan

**Goal:** Generate the complete, detailed lesson plan content.

Now that the key decisions are confirmed, generate the **full content** for all sections:

### Sections to generate (in this order):

1. **מטרות השיעור** — Three-part objectives:
   - הבנה: 3–6 bullets ("התלמידים יבינו/יכירו/ילמדו...")
   - התנסות: 2–4 bullets ("התלמידים יתנסו...")
   - יצירה: 1–2 bullets ("התלמידים ייצרו...")

2. **עזרים והכנה לשיעור** — Materials list (computers, tools, portal config, etc.)

3. **חומרים ללמידה** — Self-study resources for the instructor

4. **מבנה השיעור (90 דקות):**
   - **הקדמה (כ-5 דקות)** — Ice-breaker + intro. Bullets: לעורר עניין, להסביר
   - **ההבנה (כ-20 דקות)** — Theory delivery. Bullets: ללמד, לדון, להעריך
   - **התנסות (כ-20 דקות)** — Hands-on practice. Bullets: להדגים, להתנסות, לעזור
   - **יצירה (כ-35 דקות)** — Personal creation. Bullets: הגדרת המשימה, סיעור מוחות, הדרכה, שיתוף
   - **סיכום (כ-5 דקות)** — Wrap-up. Bullets: סיכום, משוב, תרגול (רשות)

5. **זמנים מתים** — Filler activities for when the class moves faster than expected

6. **הערכה** — How to evaluate lesson success (3–4 metrics)

7. **הערות למדריך** — Instructor tips and reminders

**Present the full plan in readable Hebrew (not JSON).** Ask for final approval.

---

## Phase 5: Handoff to DOCX

Once the user approves the full plan:

1. **Save the content as JSON** at `/home/claude/lesson_content.json` following the schema below
2. **Tell the user** you're now generating the formatted .docx
3. **Read and follow the `kidma-lesson-docx` skill** to produce the branded document

### JSON Schema

```json
{
  "lesson_number": "6",
  "title": "מוזיקה עם בינה מלאכותית",
  "objectives": {
    "understanding": ["bullet 1", "bullet 2", "..."],
    "experimentation": ["bullet 1", "bullet 2"],
    "creation": ["bullet 1"]
  },
  "materials": ["מחשב עם אינטרנט", "..."],
  "learning_materials": "Free text with links for instructor self-study",
  "structure": {
    "introduction": {
      "description": "Phase description paragraph",
      "bullets": [
        {"label": "לעורר עניין:", "text": "..."},
        {"label": "להסביר:", "text": "..."}
      ]
    },
    "understanding": {
      "description": "Phase description paragraph",
      "bullets": [
        {"label": "ללמד:", "text": "..."},
        {"label": "לדון:", "text": "..."},
        {"label": "להעריך:", "text": "..."}
      ]
    },
    "experimentation": {
      "description": "Phase description paragraph",
      "bullets": [
        {"label": "להדגים:", "text": "..."},
        {"label": "להתנסות:", "text": "..."},
        {"label": "לעזור:", "text": "..."}
      ]
    },
    "creation": {
      "description": "Phase description paragraph",
      "bullets": [
        {"label": "הגדרת המשימה:", "text": "..."},
        {"label": "סיעור מוחות:", "text": "..."},
        {"label": "הדרכה:", "text": "..."},
        {"label": "שיתוף:", "text": "..."}
      ]
    },
    "summary": {
      "description": "Phase description paragraph",
      "bullets": [
        {"label": "סיכום:", "text": "..."},
        {"label": "משוב:", "text": "..."},
        {"label": "תרגול (רשות):", "text": "..."}
      ]
    }
  },
  "dead_time": "Filler activities description",
  "assessment": "How to evaluate lesson success",
  "instructor_notes": "Tips and guidance for the instructor"
}
```

All text values must be in **Hebrew**.

---

## Language & Tone Rules

- **Conversation with the user:** Match the user's language (Hebrew or English — follow their lead)
- **All lesson content:** Always in Hebrew
- **Instructor-facing text:** Second person plural ("הדריכו את התלמידים...")
- **Warm, encouraging tone** throughout
- **Bold** key terms and concepts
- **Everyday metaphors:** cooking, puzzles, LEGO, friends, travel
- **Technical terms bilingual:** "למידת מכונה (Machine Learning)"
- **Two content layers:**
  - Surface (for students): simple analogies, 1–2 sentence explanations
  - Depth (for instructor): technical details, self-study links

## Pedagogical Principles Checklist

Before finalizing, verify these are woven in:

- [ ] "The Prompt is King" — prompt quality emphasized throughout
- [ ] Start from the End — output defined first, then working backwards
- [ ] Role-Based Prompting — students assign roles to AI
- [ ] Domain Vocabulary — professional terms introduced (Hebrew + English)
- [ ] Hebrew → English → AI → Hebrew pipeline — workflow made explicit
- [ ] Iteration is Expected — "you won't get it right the first time"
- [ ] Process Over Product — assessment evaluates journey, not just output
- [ ] Peer Collaboration — brainstorming and sharing built into creation phase
- [ ] Paper First, Screen Second — especially for visual/creative lessons

## Deep Dive Reference

For the full analysis of patterns, examples, and edge cases → read `references/deep-dive.md`.

**Read the deep dive when:**
- You need specific examples of how analogies are structured in real lessons
- You want more detail on the two-layer content depth pattern
- You're designing a Format B task sheet (entrepreneurship/workshop)
- You're unsure about any structural element

## Format B: Task Sheets

For **Entrepreneurship Workshop** or **self-directed sessions**, use Format B instead. Format B is student-facing with numbered tasks:

Each task contains:
1. Task title and number
2. Task type (learning / research / brainstorming / writing)
3. 5–6 numbered instructions, starting with "Ask the AI to..."
4. AI tool type specified
5. Expected output description

Tasks progress: learning → research → brainstorming → creation → synthesis.
Final task is always a consolidation.

**For Format B, the collaborative flow still applies** — propose the task sequence, get approval, then generate full content.
