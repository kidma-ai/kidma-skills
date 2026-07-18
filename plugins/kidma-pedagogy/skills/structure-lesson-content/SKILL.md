---
description: "Extract and reverse-engineer comprehensive raw content from Kidma lesson materials (lesson plans, presentations, task sheets) into a structured bilingual (Hebrew + English) markdown knowledge base file. Use this skill whenever the user asks to extract content from a Kidma lesson, reverse-engineer a lesson plan, create a knowledge base entry from lesson materials, process a מערך שיעור or דף הנחיות, or says anything like 'extract this lesson', 'process this lesson plan', 'reverse engineer this session', 'add this to the knowledge base', or provides Kidma lesson documents/links for content extraction. Also trigger when the user provides Google Docs/Slides links to Kidma lesson materials and asks to analyze or document them. This skill is for EXTRACTION only — it reads existing materials and outputs structured content. It does NOT generate new lessons."
type: extraction
depends_on: []
invokes: []
input_format: "file|url"
output_format: markdown
output_file: "/mnt/user-data/outputs/kidma_lesson_*.md"
runtime_tools:
  - google_drive_fetch
  - google_drive_search
requires_network: true
---

# Kidma Lesson Content Extractor

## Purpose

Reverse-engineer Kidma lesson materials into comprehensive, structured, bilingual (Hebrew + English) markdown files. The goal is to build a knowledge base of ALL Kidma lesson content — preserving every detail, never summarizing, never inventing.

## Core Principle

**Extract EVERYTHING. Summarize NOTHING.**

The output must contain every piece of information from the source materials. If content exists in the source, it must appear in the output. The structured format organizes content — it does not reduce it.

## Input Types

The skill accepts one lesson at a time. A lesson may include:

1. **Lesson plan document** (מערך שיעור / דף הנחיות) — the primary source
   - Google Docs link → use `google_drive_fetch` to read
   - Uploaded `.docx` file → read from `/mnt/user-data/uploads/`
   - Uploaded `.pdf` file → extract text using pdf-reading skill

2. **Presentation** (מצגת) — supplementary visual content
   - **ALWAYS try to find the presentation.** Presentations are a critical source of content that often contains visuals, examples, and explanations NOT found in the lesson plan document. Do not skip this step.
   - **Search strategy (in order of priority):**
     1. **User-provided file:** If the user uploads a `.pptx` file → read using pptx skill from `/mnt/user-data/uploads/`
     2. **User-provided link:** If the user provides a Google Slides or Canva link → use `google_drive_fetch` for Google Slides, or note Canva links (cannot be fetched programmatically)
     3. **Active Google Drive search:** If no presentation is provided, **proactively search Google Drive** for it:
        - Search using `google_drive_search` with queries combining the lesson topic name in Hebrew + "מצגת" (presentation)
        - Also try the lesson number + program name (e.g., "שיעור 8 מתקדמים" or "חינוך פיננסי מצגת")
        - Look for `.pptx` files, Google Slides, or PDFs that match the lesson topic
        - If found → fetch and extract content using the appropriate tool
     4. **Fallback:** Only if all search attempts fail, note "Presentation not found after active search of Google Drive" in Section 10
   - **Known Canva folder** (for reference, not programmatically accessible): https://www.canva.com/folder/FAFn4wYOkdc
   - **Tip:** Kidma presentations are often created in Canva but may also be exported and stored in Google Drive as `.pptx` files or PDF exports. Always search before giving up.

3. **Supporting documents** — task sheets, worksheets, prompt templates
   - Same input methods as above

## Workflow

### Step 1: Identify and Read All Source Materials

Ask the user what materials they have for this lesson. Then read ALL of them before starting extraction.

**For Google Docs/Slides links:**
```
Use google_drive_fetch with the document ID extracted from the URL.
```

**For uploaded files:**
```
Read the appropriate skill (file-reading, pdf-reading, pptx) 
then access files from /mnt/user-data/uploads/
```

**Proactive presentation search (ALWAYS do this):**
Even if the user doesn't mention a presentation, **always search Google Drive** for one before starting extraction. Presentations often contain unique content (diagrams, visual examples, simplified explanations) that enriches the extraction significantly.

Search approach:
1. Extract the lesson topic from the lesson plan document (e.g., "חינוך פיננסי", "טקסט לתמונה")
2. Run `google_drive_search` with:
   - `api_query`: `fullText contains 'מצגת' and fullText contains '[lesson topic in Hebrew]'`
   - Also try: `name contains '[lesson topic keyword]'` with `mimeType = 'application/vnd.google-apps.presentation'`
   - Also try broader: `name contains 'מצגת' and fullText contains '[lesson topic keyword]'`
3. If results are found, fetch the most relevant one using `google_drive_fetch` (for Google Slides) or download and read (for `.pptx`)
4. If no results from topic search, try searching by lesson number and program: e.g., `fullText contains 'שיעור 8' and fullText contains 'מתקדמים'`

**Important:** Read the FULL content of every source document. Do not skim. Do not sample. Read everything.

### Step 2: Identify the Document Format

Determine which format this lesson uses:

- **Format A: Instructor Guide (מערך שיעור למדריך)** — Written for the instructor. Contains teaching script, theory explanations, timing, classroom management notes. Follows the 4-phase structure (הקדמה → הבנה → התנסות → יצירה → סיכום). Used in Advanced A, some Advanced B, and Teaching Staff programs.

- **Format B: Task Sheet (דף הנחיות / הנחיות לעבודה)** — Written for the student. Contains numbered missions/tasks with step-by-step instructions, AI tool specifications, and expected outputs. Used in Entrepreneurship Workshop, some Advanced B lessons.

- **Hybrid** — Contains elements of both formats.

### Step 3: Extract Content Using the Template

Read `${CLAUDE_PLUGIN_ROOT}/references/output-template.md` for the exact output structure.

**Extraction rules:**

1. **Language-separated output:** The file has two parts:
   - **Part A (English):** Complete translated content — this is the primary readable content
   - **Part B (Hebrew Source):** Original Hebrew text organized by matching section numbers for cross-reference
   - The source language is declared in the metadata header
   - English content comes FIRST. Hebrew source comes SECOND. Never interleave them.

2. **Part A must stand alone:** A reader should be able to read Part A (English) and understand the entire lesson without looking at Part B. Translate everything — instructor scripts, theory, prompts, notes.

3. **Part B preserves originals verbatim:** Copy the original Hebrew text exactly as written in the source. Do not summarize. Do not paraphrase. This is the archival record.

4. **Extract ALL theory content:** Every concept, analogy, metaphor, technical explanation — in full. This includes content marked as "for instructor deepening" or "background material."

5. **Extract ALL prompts and examples:** Every example prompt, every sample output described, every comparison exercise — verbatim in both parts.

6. **Extract ALL activity instructions:** Every step of every activity, including setup instructions, brainstorming guidance, and submission requirements.

7. **Preserve structure and hierarchy:** If the lesson plan has numbered steps, sub-sections, or nested instructions, preserve that structure in the output.

8. **Flag what's missing:** If a section in the template has no corresponding content in the source, write "Not found in source materials" — never leave a section empty and never fabricate content.

9. **Capture metadata:** Program name, lesson number, duration, tools used, portal configuration, presentation link if known.

### Step 4: Handle Presentations

By this point you should have already searched for and (hopefully) fetched the presentation in Step 1. If a presentation was found:

1. Extract text from each slide
2. Note visual descriptions where text alone doesn't capture the content (e.g., "Slide shows a diagram of neural network layers")
3. Integrate presentation content into the relevant sections of the template — don't create a separate "presentation" section. Instead, add presentation content where it belongs (e.g., a slide explaining diffusion models goes into the Theory section).
4. If the presentation contains content NOT in the lesson plan, add it to the appropriate section with a note: `[From presentation]`
5. Also list slide-by-slide content in Section 10 for archival purposes

If no presentation was found despite active search, note in Section 10:
- "Presentation not found after active search of Google Drive. Searched queries: [list the queries attempted]."
- This makes it clear that search was attempted (not just skipped) and helps future users know what was tried.

### Step 5: Create the Output File

Save the extracted content as a markdown file:

**Filename convention:** `kidma_lesson_[program]_[number]_[short_topic].md`

Examples:
- `kidma_lesson_advA_01_intro_to_ai.md`
- `kidma_lesson_advA_03_text_to_image.md`
- `kidma_lesson_advB_03_data_collection.md`
- `kidma_lesson_entrepreneurship_04_brand_design.md`
- `kidma_lesson_or_v1_05_product_to_process.md`

Save to `/mnt/user-data/outputs/` and present to the user.

### Step 6: Quality Checklist

Before presenting the output, verify:

- [ ] **Presentation was actively searched for** in Google Drive (not just skipped)
- [ ] Every section of the template is present (even if marked "not found")
- [ ] All Hebrew content has English translations
- [ ] No content from source materials was omitted
- [ ] Theory content is extracted in full, not summarized
- [ ] All prompts and example prompts are included verbatim
- [ ] All activities have complete step-by-step instructions
- [ ] Tools, portal config, and assessment criteria are captured
- [ ] Source documents are listed in the metadata
- [ ] Filename follows the naming convention

## What This Skill Does NOT Do

- Does NOT generate new lesson plans (that's a different skill)
- Does NOT evaluate or critique the lesson content
- Does NOT reorganize content to "improve" it — it preserves the original structure
- Does NOT add information not present in the source materials
- Does NOT summarize — it extracts in full

## Output Template

The complete output template with all sections and formatting is in `${CLAUDE_PLUGIN_ROOT}/references/output-template.md`. **Always read it before starting extraction.**
