---
description: "Generate two Nano Banana (Gemini) image prompts for a Kidma article. Takes the article content and produces two ready-to-paste prompts — one in a warm documentary photography style and one in a bold conceptual illustration style — both aligned to the Kidma brand and visual identity. Use when you have a finished or draft article and need a hero image or in-article image prompt to generate via Nano Banana. Triggers: 'generate image prompt for this article', 'create image prompts', 'Nano Banana prompt for article', 'article image', 'hero image prompt', 'image for the article'."
type: interactive
depends_on:
  - kidma-plugins:overview
  - kidma-plugins:brand
invokes: []
output_format: text
---

# Kidma: Article Image Prompt Generator (Nano Banana)

Produce two Nano Banana image prompts for a Kidma article — one per visual style — so the author can pick the one that best fits the piece. Output is two labeled, paste-ready English prompts printed to chat.

## 0. At session start — read these first

- `kidma-plugins:overview` — company context, audience (school principals), programs, Israeli education setting.
- `kidma-plugins:brand` — Kidma color palette (Blue #2669F6 · Light Green #93DC88 · Pink #FF70A3), methodology color code (Understand=Blue / Try=Green / Create=Pink), visual principles (clean, minimal, RTL).

## 1. What you receive

The human provides an article. It will be:
- A full `.md` block (output of the `write-article` skill) with YAML frontmatter + Hebrew body, or
- A partial draft or description of what the article covers.

If only a description is given, ask for the full article or at minimum: **topic**, **key claim**, **category** (`מחקר` / `פדגוגיה` / `קהילה` / `נתונים`), and **suggestedAccent** (`blue` / `green` / `pink`).

## 2. Silent analysis — extract before generating

Before writing any prompt, identify these fields from the article. Do **not** print this analysis; let it silently inform the prompts.

| Field | What to extract | Fallback if unclear |
|-------|----------------|---------------------|
| **Core subject** | The central topic or scenario | Ask |
| **Key visual element** | The one concrete thing the image should evoke (classroom discussion, student at a laptop, a principal reviewing data, abstract growth metaphor) | Derive from article body |
| **Primary tone** | Hopeful? Challenging? Investigative? Celebratory? Warm? | Infer from writing style |
| **Methodology stage** | Understand (Blue) / Try (Green) / Create (Pink) | Use `suggestedAccent` if present; otherwise infer |
| **People in image** | Principal? Teacher? Student? No people? | Infer from article's audience and subject |
| **Image placement** | Hero (full-width, article top) or body (inline illustration) | Default to hero unless specified |

## 3. The two Kidma image styles

### Style A — "Warm Documentary" (Photorealistic Photography)

A realistic scene from an Israeli school context. Real-looking people, a specific and authentic moment, soft natural or warm ambient lighting. The image should make a school principal think: *I see myself, my school, my teachers here.*

**Elements to include in the prompt:**
- **Setting:** Israeli school — classroom, teachers' lounge, corridor, computer lab, outdoor yard, or meeting room. Specific, not generic.
- **People:** match to the article's subject — school principal (40s–60s), teachers (30s–50s), or students (elementary through high school). Feature one or two people, not a crowd.
- **Action:** a specific, meaningful moment — a thoughtful conversation, reviewing something on a tablet, pointing at a whiteboard during discussion, collaborative work between two people.
- **Lighting:** soft natural light from windows, or warm indoor ambient. Never harsh flash or harsh overhead fluorescent.
- **Style terms:** documentary portrait, editorial photography, candid reportage, photojournalistic.
- **Framing:** medium shot or close-up. Avoid wide architectural shots.
- **Technical:** sharp focus on the subject, soft background bokeh, high resolution.
- End the prompt with: `No text in the image.`

**Avoid:**
- Generic Western stock photo polish (too diverse, too staged)
- Dystopian or anxious subjects
- "Pointing at whiteboard" unless genuinely relevant to the article

### Style B — "Bold Conceptual" (Graphic Illustration)

A clean, graphic illustration that captures the article's central *idea* as a visual metaphor. Uses Kidma brand colors directly. No photorealism — this is editorial design or conceptual flat art.

**Elements to include in the prompt:**
- **Style terms:** flat vector illustration, editorial graphic, conceptual poster art, graphic design.
- **Color palette:** lead with the Kidma methodology color matching the article's stage:
  - `Blue (#2669F6)` — Understand content (research, analysis, learning theory)
  - `Light Green (#93DC88)` — Try content (experimentation, activities, process)
  - `Pink (#FF70A3)` — Create content (creativity, projects, making)
  - Pair with off-white (`#F3F3F3`) background or dark (`#292920`) background.
- **Subject:** a visual metaphor using objects, shapes, or symbols — not realistic people. Examples: a sprouting seedling for growth, interlocking puzzle pieces for collaboration, a magnifying glass for inquiry, a lightbulb broken into three colored fragments.
- **Composition:** bold, centered or rule-of-thirds, generous whitespace. RTL-aware: visual weight toward the right side.
- **Mood:** modern, clean, purposeful. No decorative clutter.
- End the prompt with: `No text in the image.`

**Avoid:**
- Colors outside the Kidma palette as dominant tones
- Photorealistic or 3D-render style
- Overly complex scenes
- Generic clipart or cartoon style

## 4. Output contract

After the silent analysis, print exactly two labeled prompt blocks to chat. No lengthy preamble — open directly with the prompts.

```
---

**Style A — Warm Documentary Photography**

`[Full Nano Banana prompt, 2–4 sentences, self-contained English, ready to paste]`

---

**Style B — Bold Conceptual Illustration**

`[Full Nano Banana prompt, 2–4 sentences, self-contained English, ready to paste]`

---

> **המלצה:** [One Hebrew sentence recommending which style fits better and why, grounded in the article's category and tone.]
```

Nothing else. The user picks one and pastes it into Nano Banana.

## 5. Quality checks before outputting

- Prompt A describes a real, observable educational moment — not a posed stock photo cliché.
- Prompt B references at least one Kidma brand color by hex value or explicit name.
- Neither prompt contains instructions to add text or logos to the image.
- Both prompts are complete, grammatical English sentences — passable to Nano Banana without editing.
- The recommendation is grounded in the actual article content, not generic advice.
- Neither prompt depicts anything inappropriate for a school audience.

## 6. When to stop and ask

Stop generating and ask the human if:

- The article is too vague to determine a meaningful key visual element.
- `suggestedAccent` is absent and the topic could belong to any methodology stage — a wrong color choice undermines the brand.
- The article discusses a sensitive topic (school failure, conflict, trauma) where a poorly chosen image could be misread.
- The human specifies a particular placement (full-bleed hero vs. inline body image) that changes composition requirements.

## 7. Example output

Given a `פדגוגיה` article about teachers building confidence with AI tools in class (suggestedAccent: `blue`):

---

**Style A — Warm Documentary Photography**

`A female Israeli school teacher in her forties sits at a classroom desk, leaning toward a laptop screen with a focused, curious expression. A student sits nearby, half in frame. Soft morning light filters through large classroom windows behind them. Documentary editorial photography, medium shot, warm natural tones, shallow depth of field. No text in the image.`

---

**Style B — Bold Conceptual Illustration**

`Flat vector illustration of a large open laptop screen casting blue light (#2669F6) onto two simplified silhouettes — a larger adult figure guiding a smaller student figure. Clean off-white background (#F3F3F3). Minimalist editorial graphic design, bold blue and white palette with a single thin light-green (#93DC88) accent arc. Generous whitespace, balanced composition, visual weight toward the right. No text in the image.`

---

> **המלצה:** לכתבה פדגוגית שמתארת תהליך רגשי של מורות שמתגברות על פחד, סגנון A יוצר חיבור אנושי חזק יותר — אם הכתבה מנתחת מגמה או מציגה ממצאים, סגנון B יתאים יותר.

---

## Related Skills

- **`kidma-plugins:write-article`** — Produces the article this skill consumes. The `heroDescription` and `suggestedAccent` frontmatter fields are the primary inputs.
- **`kidma-plugins:brand`** — Required. Defines the color palette and visual principles applied in Style B.
- **`kidma-plugins:overview`** — Required. Ensures the Israeli school setting and Kidma audience are reflected in Style A.
