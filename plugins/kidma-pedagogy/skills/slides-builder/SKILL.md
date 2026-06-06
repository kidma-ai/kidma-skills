---
description: "Build a Kidma lesson presentation .pptx file from an approved presentation plan. This skill is the FILE CREATION counterpart to the slides-planner skill. ALWAYS use this skill when you have a finalized, user-approved presentation plan (slide sequence, content, types) and need to generate the actual .pptx file. Also trigger when the user says 'now build the file', 'create the pptx', 'generate the presentation file', or when the planner skill hands off an approved plan. This skill handles template manipulation, slide XML editing, QA, and file output — it does NOT handle content planning or user collaboration (that's the planner's job). Always read the pptx skill first."
type: generation
depends_on:
  - kidma-plugins:brand
invokes: []
input_format: text
input_file: "/home/claude/presentation_plan.txt"
output_format: pptx
output_file: "/mnt/user-data/outputs/presentation.pptx"
runtime_tools:
  - bash
python_packages:
  - python-pptx
---

# Kidma Presentation Builder

This skill takes an **approved presentation plan** (from the kidma-presentation-planner skill or user) and generates a .pptx file using the official Kidma template.

**This skill handles file creation only.** It assumes content has already been planned and approved. If no approved plan exists, redirect to the `kidma-presentation-planner` skill first.

## Prerequisites

Before starting, **always read these skills:**
- `the pptx public skill` — for the pptx creation/editing workflow
- `the pptx editing reference` — for the template-based editing workflow
- `kidma-plugins:brand skill` — for Kidma's official colors, typography, logo variants, and light/dark mode rules. Use when adding new slides, picking accent colors, or inserting logos beyond what the template provides.

The Kidma template is at: `${CLAUDE_PLUGIN_ROOT}/assets/template.pptx`

---

## Step 1: Validate the Plan

Before building, verify the approved plan includes:
- [ ] Total slide count (10-15)
- [ ] For each slide: template slide number, all text content
- [ ] Cover slide with title, subtitle, description, lesson number
- [ ] Summary slide with 4 takeaways + closing question
- [ ] Task slide with specific AI tool names
- [ ] No two consecutive slides use the same template layout

If anything is missing, ask the user to clarify before proceeding.

---

## Step 2: Build the Presentation

Follow the **pptx editing workflow** from `the pptx editing reference`:

### 2.1 Copy and Unpack

```bash
cp ${CLAUDE_PLUGIN_ROOT}/assets/template.pptx /home/claude/template.pptx
python /mnt/skills/public/pptx/scripts/office/unpack.py /home/claude/template.pptx /home/claude/unpacked/
```

### 2.2 Plan Slide Operations

Based on the approved plan, determine:
- **Which template slides to keep** as-is (just edit content)
- **Which template slides to duplicate** (using `add_slide.py`)
- **Which template slides to delete** (remove unused ones)
- **Final slide order** (reorder `<p:sldId>` in `ppt/presentation.xml`)

**Always delete Slide 1** (template instruction slide) — remove its `<p:sldId>` from `ppt/presentation.xml`.

### 2.3 Execute Slide Operations

1. **Duplicate** needed slides using `add_slide.py`
2. **Delete** unused slides by removing their `<p:sldId>` entries
3. **Reorder** `<p:sldId>` elements to match the planned sequence

### 2.4 Edit Content

For each slide XML, replace placeholder text with the approved content.

Read `references/slide-catalog.md` for the exact placeholder text in each template slide. The general pattern:

| Placeholder | Replace With |
|---|---|
| `כותרת פיקנטית` | Lesson title (Cover slide only) |
| `כותרת` | Section/concept title |
| `תיאור` | Description text |
| `תוכן` | Content label |
| `משפט אחד` / `שני` / `שלישי` | Bullet points |
| `נושא 1` through `נושא 4` | Topic names |
| Tool badge text ("Gemini", etc.) | Actual tool names |

### 2.5 Clean and Pack

```bash
python /mnt/skills/public/pptx/scripts/clean.py /home/claude/unpacked/
python /mnt/skills/public/pptx/scripts/office/pack.py /home/claude/unpacked/ /home/claude/output.pptx --original /home/claude/template.pptx
```

---

## Step 3: QA

Follow the pptx skill's QA workflow:
1. Convert slides to images
2. Visually inspect each slide
3. Verify:
   - All placeholder text has been replaced (no "כותרת" or "תיאור" leftovers)
   - Text is RTL and in Hebrew
   - Fonts are Rubik/Calibri
   - No duplicate consecutive layouts
   - Cover is first, Summary is last
   - Tool badges on task slide show correct tool names
   - Copyright footer and Kidma logo are intact

If issues are found, fix and re-pack.

---

## Step 4: Output

Copy the final file to the output directory and present to the user:

```bash
cp /home/claude/output.pptx /mnt/user-data/outputs/[lesson-name]-presentation.pptx
```

Use `present_files` to share with the user.

---

## Content Rules (enforce during editing)

- **All text RTL** — Hebrew throughout
- **Fonts & Colors:** See `kidma-plugins:kidma-brand-guidelines skill`
- **Technical terms bilingual:** "למידת מכונה (Machine Learning)"
- **Concise:** Max 3 bullet points per content slide
- **Emojis:** Use where template uses them: 📖 💬 🤖 ✨ 🎨 ❌ ✅ 💡 🎯 🤔
- **Copyright footer** — inherited from template, don't modify
- **Kidma logo** — inherited from template, don't modify

---

## Template Layout Reference

| Layout | Slides | Visual |
|--------|--------|--------|
| TITLE_1 | 1, 2 | Cloud background, large centered title |
| BLANK_1 | 3, 13–21 | White bg, Kidma logo, copyright footer |
| BLANK_1_2 | 10, 22 | White bg + corner colored shapes |
| BLANK_1_2_1 | 11, 12 | White bg + dual corner shapes |

---

## Reference Files

Read `references/slide-catalog.md` for:
- Exact visual description of every template slide
- All text placeholders and what to replace
- Color details for decorative elements
- Which slides work for specific content types

---

## Also Creates: Lesson Summary (סיכום שיעור)

If the user also requests a post-lesson student summary, read `references/summary-patterns.md` for the exact structure and formatting rules. Create as `.docx` (read `the docx public skill` first) or `.md` file.

### Summary Quick Reference

Structure:
```
# שיעור [N] — [Topic]
[Practical subtitle]

## מושגי יסוד
**Hebrew — English** — definition
...

## [Content Section]
...
```

Rules:
- מושגי יסוד is ALWAYS first section
- 2-4 content sections after key concepts
- Hebrew, student-facing, warm, accessible
- Bold all key terms
- 1-2 pages max
- No instructor content
