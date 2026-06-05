---
description: "Draft a complete Hebrew article for Kidma writing surfaces (kid-ma.com /articles, newsletters, LinkedIn posts, school proposals). Produces a single `.md` content block — frontmatter + Markdown body — printed to chat for human review. Does NOT handle site-specific embedding, MDX components, file placement, or git workflow — those belong to the consuming surface (e.g., the kidma-site repo's `publish-article` skill). Use this skill when the user asks to write, draft, or generate an article, blog post, or piece of long-form content for Kidma. Depends on `kidma-plugins:overview` (company facts, audience, programs) and `kidma-plugins:brand` (brand colors, methodology code, slogan formatting) — both must be read at session start. Triggers: 'write an article', 'draft an article', 'new article about X', 'cornerstone piece for principals', 'write content for Kidma'."
type: interactive
depends_on:
  - kidma-plugins:overview
  - kidma-plugins:brand
invokes: []
output_format: markdown
---

# Kidma: Write an Article (Content Generator)

Produce the `.md` content of a Hebrew article aimed at school principals. Output is a single chat-printed Markdown block — no files written, no site plumbing. A separate publisher skill (kidma-site's `publish-article`) consumes this output and embeds it into the site.

## 0. At session start — read these first

Two foundation skills carry context this skill relies on. **Read both before generating any content.** Do not duplicate their content inline; refer to them.

- `kidma-plugins:overview` — company facts, audience definition (school principals + senior education staff), programs, partners, founders, 2028 vision. Drives whether a claim is on-brand and whether a named partner/educator is verifiable.
- `kidma-plugins:brand` — full color palette, methodology code (Understand=Blue · Try=Green · Create=Pink), slogan formatting rules, typography. Drives the `suggestedAccent` frontmatter value.

**One writing principle that supersedes everything else:**
Kidma's writing surfaces exist to move a principal closer to booking an intro meeting. Every article must be evaluable against this — does it earn that meeting, or distract from it? The publisher will insert the actual call-to-action; the writer's job is to produce prose that *earns* it.

## 1. Inputs required from the human

Before generating, confirm you have all of:

| Input | Example | If missing |
|-------|---------|------------|
| Topic | "Why principals fear AI rollouts and how to reframe" | Ask. |
| Key claim | "Fear is rational; the fix is structural, not motivational." | Ask. |
| Evidence | Links, quotes, internal data, or "exploratory — illustrative is fine" | Ask; never invent stats silently. |
| Length | short / medium / long (see §3) | Default to medium, confirm. |
| Author | Name + initials | Ask. |
| Category | `מחקר` \| `פדגוגיה` \| `קהילה` \| `נתונים` | Suggest one, confirm. |

If any are unclear, **ask before generating**. Cheap to ask, expensive to rewrite a 1,000-word Hebrew article.

## 2. Voice and tone

**Audience** (per `kidma-company-overview`): school principals and senior education staff. Time-pressed, decision-makers, mildly skeptical of edtech hype.

**Do:**
- Hebrew, formal but warm. Address the reader as "אתם" or rephrase impersonally.
- Concrete over abstract. Name a school year, a class size, a tool, a number.
- Evidence-first: if you claim "78% of teachers feel X," cite a source — or mark the figure explicitly as illustrative ("בדוגמה היפותטית").
- Acknowledge complexity. Principals distrust pieces that pretend the problem is simple.

**Don't:**
- No hype words: "מהפכני", "מדהים", "פורץ דרך", "המסע", "DNA".
- No exclamation marks in body prose (titles fine if rare).
- No emojis anywhere.
- No clickbait framing ("הסוד ש...", "מה שאף אחד לא אומר על...").
- No second-person singular ("אתה") — too informal for the audience.
- Don't fake testimonials, school names, or partner endorsements. Real names only when verified by the human, otherwise generic ("מנהלת חט"ב במרכז הארץ").
- Don't invent competitor comparisons.

**Slogan use:** Follow `kidma-brand-guidelines` formatting exactly ("מבינים. מנסים. יוצרים." with periods as separators). Use at most once per article, and only when the body has earned it — i.e., you've actually discussed the three pillars.

**Do not write any call-to-action.** The publisher inserts that. Your job is prose that makes the CTA feel earned, not to write the CTA itself.

## 3. Length and structure

| Length | Hebrew words | Read time | When |
|--------|--------------|-----------|------|
| Short  | ~600         | 4 min     | Single sharp point, opinion piece. |
| Medium | ~1,100       | 7 min     | **Default.** Most cornerstone pieces. |
| Long   | ~1,700+      | 10+ min   | Research summary, multi-stakeholder topic. |

**Default skeleton** (use unless the topic clearly demands otherwise):

1. **Opening hook** — 1–2 paragraphs. Concrete scenario or surprising-but-credible data point. No throat-clearing.
2. **What's actually going on** — 2–3 paragraphs. Frame the problem from a principal's vantage.
3. **What it looks like in practice** — 2–4 paragraphs. Examples, evidence, what Kidma has seen in the field. This is the load-bearing section.
4. **What to do about it** — 2–3 paragraphs. Actionable for a principal *this term*, not "in five years."
5. **Close** — 1 short paragraph. Tie back to the opening.

Use `##` for the 4–5 section headings. Use `###` sparingly for sub-points. **Never use `#`** — the publisher renders the frontmatter title as the page h1.

Don't pad. Better short and dense than long and thin. If you can't reach the target length without filler, ask the human for more material.

## 4. Images

Reference images by descriptive filename without path prefixes — the publisher will resolve and colocate them:

```md
![תלמידי כיתה ה׳ עובדים בזוגות מול מחשב נייד.](classroom-laptop.jpg)
```

- **Alt text is required, in Hebrew, and meaningful.** Not acceptable: `![תמונה](...)`, `![hero](...)`, empty alt.
- **Do not generate AI images for articles.** Kidma reserves AI-generated cinematic photography for one specific surface (the home hero); everywhere else uses real photography or flat-vector illustration.
- **Do not pull stock photos** without the human's approval (licensing risk).
- The hero image goes in the frontmatter (`heroDescription`), not the body — describe what it should depict and the publisher will prompt the human for the actual file.

## 5. Output contract

After all inputs are gathered, print exactly one Markdown block to chat, shaped like this:

````md
---
title: 'הפחד של המורה מ-AI — ולמה הוא הגיוני לחלוטין'
excerpt: 'שיחה עם 14 מורות שחששו מ-AI ועכשיו מלמדות עם כלים בכל שיעור. מה שינה להן את הראש?'
author: 'נועה ברק'
authorInitials: 'נב'
date: '2026-04-12'
category: 'קהילה'
suggestedAccent: pink
heroDescription: 'תקריב על מורה מבוגרת מחייכת מול מסך מחשב נייד, בכיתה עם תלמידי חטיבת ביניים מטושטשים ברקע. תאורה רכה, אווירה אופטימית.'
lengthTarget: medium
---

(Body in Hebrew, pure Markdown, following the §3 skeleton.)
````

**Frontmatter field rules:**
- `title`: 30–80 Hebrew characters. Don't end with a period. Em-dash (`—`) OK.
- `excerpt`: 90–180 Hebrew characters. One sentence. Ends with a period or question mark. Will be used as both meta description and listing-card body — write for both.
- `date`: ISO `YYYY-MM-DD`. Use the planned publish date, not the drafting date.
- `category`: exactly one of the four Hebrew options.
- `suggestedAccent`: one of `blue`, `green`, `pink`. Match the article's *intent* (Understand=blue, Try=green, Create=pink), not the category. Pink is rare — only when the piece is genuinely about creating/making. The publisher may override.
- `heroDescription`: **mandatory**. A Hebrew sentence (or two) describing what the hero image should depict. The publisher uses this to prompt the human for the actual image file before publication. Be specific enough that the human knows what to source.
- `lengthTarget`: one of `short`, `medium`, `long`. Helps the publisher set `readMinutes` if not pre-computed.

**After printing the block**, repeat the `heroDescription` separately as a "Hero image needed:" callout at the top or bottom of your reply, so the human notices it and can start sourcing the image while reviewing the prose.

## 6. When to stop and ask

Stop generating and ask the human if:

- You can't find evidence for a load-bearing claim and the topic isn't explicitly flagged exploratory.
- The piece would name a specific Israeli school, partner organization, or named educator you cannot verify against `kidma-company-overview`.
- The piece would compare Kidma against a named competitor.
- You're tempted to invent statistics, testimonials, or quotes.
- The human's brief would push the article away from the single conversion goal (book an intro meeting) — e.g., asking for a piece that promotes a different product, sells a course directly, or makes the article a thinly-veiled ad.

## 7. Reference: a minimal complete output

````md
---
title: 'שלוש שאלות לשאול לפני כל פיילוט AI בבית הספר'
excerpt: 'לפני שמטמיעים כלי, מנהלות שעובדות איתנו שואלות שלוש שאלות שמסננות 80% מהבעיות מראש.'
author: 'נועה ברק'
authorInitials: 'נב'
date: '2026-05-20'
category: 'פדגוגיה'
suggestedAccent: blue
heroDescription: 'מנהלת בית ספר בשנות הארבעים עומדת מול לוח לבן עליו נכתבו שלוש שאלות בעברית, מצביעה על השאלה האמצעית. תאורה טבעית מחלון.'
lengthTarget: medium
---

בכל פעם שאנחנו מתחילים פיילוט AI עם בית ספר חדש, השיחה הראשונה לא עוסקת
בכלי. היא עוסקת בשלוש שאלות שמנהלות מנוסות לומדות לשאול לפני שהן בכלל
שומעות הדגמה.

## מי הקהל האמיתי?

…

## מה הצלחה נראית בעוד שלושה חודשים?

…

## מה נדרש מהמורות בפועל?

…

## ולסיום

שלוש שאלות. רבע שעה. חוסכות חודשים של טיפול בבעיות שיכולנו למנוע מראש.
````

> **Hero image needed:** מנהלת בית ספר בשנות הארבעים עומדת מול לוח לבן עליו נכתבו שלוש שאלות בעברית, מצביעה על השאלה האמצעית. תאורה טבעית מחלון.

That's the entire shape. Everything else is judgment.

---

## Related Skills

- **`kidma-plugins:overview`** — Required. Company facts, audience, programs, partners.
- **`kidma-plugins:brand`** — Required. Brand colors, methodology code, slogan rules.
- **`publish-article`** (project-local in kidma-site) — Consumes this skill's output and embeds it into the kidma-site `/articles` route. Handles slug, hero image, MDX transform, branch + PR.
