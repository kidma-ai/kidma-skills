# Kidma Lesson Summary Patterns

> Patterns extracted from 15+ real lesson summaries across all Kidma programs.

## Universal Structure

Every summary follows this exact order:

```
1. Title Block
2. מושגי יסוד (Key Concepts) — ALWAYS FIRST
3. Content Block 1 (varies by lesson)
4. Content Block 2 (varies by lesson)
5. Optional: Content Block 3–4
```

---

## Title Block Pattern

**Format A (numbered series):**
```
# שיעור [N] — [Topic Name]
[Practical subtitle describing what students did]
```

**Format B (standalone):**
```
# סיכום שיעור — [Topic Name]
[Practical subtitle]
```

**Examples from real summaries:**
- `שיעור 2 — עיבוד שפה טבעית / יצירת שיר וסיפור אישי`
- `סיכום שיעור — מבוא לבינה מלאכותית`
- `סיכום שיעור בדמיון — טקסט לתמונה`
- `סיכום שיעור — השוואה שימושית`

---

## Key Concepts Section (מושגי יסוד)

This is ALWAYS the first section after the title. Format:

```
## מושגי יסוד

**Hebrew Term — English Term** — definition in accessible Hebrew

**Hebrew Term — English Term** — definition using everyday analogy
```

**Rules:**
- 2–6 terms per summary
- Bold the term pair, plain text for definition
- Use analogies where possible (cooking, friends, puzzles)
- Cover both the AI concept AND the domain knowledge
- Terms appear in order of increasing specificity

**Common terms that recur across many summaries:**
- בינה מלאכותית — Artificial Intelligence
- למידת מכונה — Machine Learning
- למידה עמוקה — Deep Learning
- בינה מלאכותית יוצרת — Generative AI
- פרומפט — Prompt
- מודל שפה גדול — Large Language Model (LLM)

---

## Content Block Types

### Type 1: Process / Steps (numbered)

**Used in:** NLP, Text-to-Image, Text-to-Speech, Face Swap, Article Writing

**Pattern:**
```
## [Process Title]

1. **שלב ראשון** — description
2. **שלב שני** — description
3. **שלב שלישי** — description
...
```

**Example topics:**
- "שלבי עיבוד המידע" (NLP processing steps)
- "תהליך הפיכת טקסט לקול" (TTS pipeline)
- "איך עובד מודל דיפוזיה?" (Diffusion process)

### Type 2: How-to Tips (bullet list)

**Used in:** Almost every lesson

**Pattern:**
```
## איך כותבים פרומפט טוב?

• **tip name** — explanation
• **tip name** — explanation
• **tip name** — explanation
```

**Variations:**
- "טיפים לכתיבת פרומפט אפקטיבי"
- "עקרונות ליצירת תמונה טובה"
- "כללים לעבודה נכונה עם AI"

### Type 3: Domain Vocabulary / Elements

**Used in:** Image generation, Music, Code, Presentations

**Pattern:**
```
## אלמנטים חשובים ליצירת [domain]

• **Element** — what it controls
• **Element** — what it controls
```

**Domain-specific vocabularies:**

| Domain | Key Terms |
|--------|-----------|
| **Image** | תאורה (lighting), צבעים (colors), זוויות (angles), מיקוד (focus), רקע (background), פלטת צבעים (color palette), מרקם (texture) |
| **Music** | טמפו (tempo), ז'אנר (genre), כלי נגינה (instruments), מצב רוח (mood) |
| **Code** | פונקציונליות (functionality), עיצוב (design), רספונסיביות (responsiveness) |
| **Text** | תפקיד (role), טון (tone), מבנה (structure), אורך (length), סגנון (style) |

### Type 4: Comparison

**Used in:** Comparison lesson, evaluating AI outputs

**Pattern:**
```
## השוואה: [Thing A] לעומת [Thing B]

| קריטריון | [A] | [B] |
|----------|-----|-----|
| ... | ... | ... |
```

Or narrative format:
```
## מתי עדיף [A] ומתי [B]?

**[A] מתאים כאשר:** ...
**[B] מתאים כאשר:** ...
```

### Type 5: Categories / Types

**Used in:** Deepfakes, Ethics, Critical Thinking

**Pattern:**
```
## סוגי [category]

• **Type 1** — description
• **Type 2** — description
```

### Type 6: Limitations

**Used in:** Image generation, Music, any tool-specific lesson

**Pattern:**
```
## מגבלות ב[tool/capability]

• Limitation 1
• Limitation 2
```

### Type 7: Prompt Template

**Used in:** Image, TTS, Avatar lessons

**Pattern:**
```
## מבנה פרומפט ל[task]

[role] + [context] + [specific details] + [constraints]

דוגמה:
"You are a professional photographer. Create a portrait photo of..."
```

---

## Lesson-Type → Section Mapping

| Lesson Topic | Section 1 (after מושגי יסוד) | Section 2 | Section 3 |
|---|---|---|---|
| Intro to AI | What is AI? (overview) | Types of AI | How AI learns |
| NLP / Text-to-Text | How NLP works (process) | Prompt writing tips | Query vs Chatbot modes |
| Text-to-Image | How diffusion works (process) | Visual vocabulary | Prompt tips |
| Comparison | When to compare | Comparison criteria | Tips for evaluation |
| Deepfakes | Types of deepfakes | How face swap works | Ethical considerations |
| AI Music | How AI makes music | Music vocabulary | Tips for good prompts |
| Financial Education | Key financial concepts | Income & expenses | Compound interest |
| Text-to-Speech | How TTS works (process) | Voice parameters | Prompt template |
| Data Collection | AI FIRST methodology | FOCUS framework | Source types |
| Self-Learning Studio | What is NotebookLM | How to build a studio | Source management |
| Entrepreneurship | Problem identification | Market research basics | Validation approach |
| Brand Design | Brand elements | Visual identity | Brand board structure |

---

## Formatting Quick Reference

| Element | Format |
|---------|--------|
| Key term | **Hebrew — English** — definition |
| Section header | ## Hebrew title |
| Bullet list | • **Bold label** — explanation |
| Numbered steps | 1. **Step name** — description |
| Prompt example | Indented or code block |
| Table | Standard markdown table |
| Image placeholder | `[image1]: <>` |
| Total length | 1–2 pages |
| Audience | Students (NOT instructors) |
| Language | Hebrew (English only for technical terms) |
