---
description: "Write Hebrew Facebook posts that promote a Kidma article already published on kid-ma.com. Takes the published article (URL + content) and produces three ready-to-paste post variants — each built on a different research-backed hook strategy (pain-point question, concrete insight, story/quote) — plus a recommendation and a publishing checklist (link preview, timing, comment follow-up). Use when an article is live and needs promotion on the Kidma Facebook page. Depends on `kidma-plugins:overview` and `kidma-plugins:brand` — both must be read at session start. Triggers: 'Facebook post', 'promote the article', 'share the article on Facebook', 'social post for the article', 'פוסט לפייסבוק', 'פוסט פייסבוק', 'לקדם את הכתבה', 'לשתף את המאמר'."
type: interactive
depends_on:
  - kidma-plugins:overview
  - kidma-plugins:brand
invokes: []
input_format: article URL + article content (md or pasted text)
output_format: text
---

# Kidma: Facebook Post for a Published Article

Produce three Hebrew Facebook post variants that promote an article already live on kid-ma.com, plus a short recommendation and a publishing checklist. Output is printed to chat — nothing is posted automatically; the human copies the chosen variant into Facebook.

## 0. At session start — read these first

- `kidma-plugins:overview` — company facts, audience (school principals + senior education staff), programs, 2028 vision. Drives which claims are on-brand.
- `kidma-plugins:brand` — slogan formatting ("מבינים. מנסים. יוצרים." — periods as separators), tone principles.

**The conversion chain:** article → intro meeting. The Facebook post's only job is one click — get the right reader (a principal or senior educator) to open the article. The article does the persuading. Do not try to make the post sell the meeting; a post that tries to do the article's job becomes an ad, and ads get scrolled past.

## 1. Inputs required from the human

| Input | Example | If missing |
|-------|---------|------------|
| Published URL | `https://kid-ma.com/articles/ai-pilot-questions` | Ask — the post cannot exist without it. |
| Article content | The `.md` from `write-article`, or pasted text | Ask for it (or fetch the URL if browsing is available). Never write a post from the title alone. |
| Anything to emphasize | "Lead with the 3-questions framework" | Optional — default to your own judgment. |

## 2. Why the post is shaped this way (the marketing logic)

These are the current, evidence-backed rules for organic link posts on Facebook. They are the reason for every constraint in §3–§4 — don't relax them for style:

1. **A bare link earns nothing.** Facebook's algorithm gives link posts little organic reach on their own; the post text must deliver standalone value that earns engagement *before* the click. Write the post so that someone who never clicks still learned one real thing.
2. **The hook must survive the fold.** On mobile, Facebook truncates after roughly 110–140 characters with an "עוד" (See more) link. The first line decides everything — it must work alone, before any context below it.
3. **Short beats long for clicks.** Posts of roughly 80–150 characters get the most link clicks; longer posts only work when they are clearly structured value (a mini-insight, a story). Target the whole post at 300–600 Hebrew characters, never more than ~800.
4. **No engagement bait, no clickbait.** "שתפו אם אתם מסכימים", "לייק למי ש...", and headlines that withhold the point ("מה שגיליתי ישנה לכם את...") are algorithmically penalized *and* off-brand for an audience of principals.
5. **Don't repeat the link preview.** The Open Graph card already shows the article's title, description, and hero image. Post text that restates the title wastes the reader's attention twice. Add a *perspective* the card doesn't show.
6. **One link, in the post body, on its own line.** The "link in first comment" trick has mixed evidence and confuses readers; for a Page promoting its own article, put the link in the post.

## 3. Voice and tone — Facebook is not the article

Same audience as `write-article` (principals, senior education staff — time-pressed, mildly skeptical of edtech hype), but the register shifts one notch warmer and more direct:

**Do:**
- Hebrew, address the reader as "אתם". Short sentences. Line breaks between thoughts — dense paragraphs die on mobile.
- Concrete over abstract: a number, a grade level, a named tool, a real moment from the article.
- First person is welcome ("ראינו את זה שוב ושוב בבתי ספר") — a Page post may sound like the team talking, not like an editorial.
- One question is fine when it's a *real* question the reader has asked themselves — not a rhetorical setup.

**Don't:**
- No hype words: "מהפכני", "מדהים", "פורץ דרך". No exclamation-mark stacking (one, rarely, is tolerable on Facebook).
- At most **one** emoji per post, and only as a functional pointer (e.g., 👇 above the link). Zero is the default.
- No hashtag walls. At most 1–2 genuinely useful ones (e.g., `#חינוך`), or none.
- Never invent statistics, testimonials, school names, or quotes — everything factual in the post must come from the article itself or from `kidma-plugins:overview`.
- The slogan "מבינים. מנסים. יוצרים." at most once, and only if the post's content earns it.

## 4. Post anatomy

Every variant follows this skeleton:

1. **Hook** — 1 line, ≤ ~110 characters, works standalone above the fold. This is 80% of the work.
2. **Value body** — 2–4 short lines that deliver one real takeaway *from the article*. The reader who stops here should still have gotten something.
3. **Bridge** — 1 line that makes the click feel like the natural next step, framed as what the reader *gets*, not what we want: "בכתבה המלאה: שלוש השאלות, ולמה השנייה הכי חשובה." Never "לחצו כאן" alone.
4. **Link** — the URL on its own final line.

## 5. The three hook strategies

Generate exactly one variant per strategy, so the human can pick the fit:

### Variant A — Pain-point question
Open with the question the principal is already asking themselves, in their words. Then the body gives the article's reframe.
*Shape:* «question they recognize» → «the surprising reframe» → bridge → link.

### Variant B — Concrete insight
Open with the single most concrete, surprising, credible fact or claim in the article — a number, a before/after, a field observation. No suspense, no withholding: state it, then add one line of context.
*Shape:* «the fact» → «why it matters to a principal» → bridge → link.

### Variant C — Story / quote
Open with a specific human moment or a strong pull-quote from the article (real quotes only — if the article has none, use a field scene it describes). Stories earn the highest share rates.
*Shape:* «the moment» → «what it revealed» → bridge → link.

If the article genuinely cannot support one of the strategies (e.g., no data point exists for B), say so in one line and produce the other two — never fabricate material to fill a template.

## 6. Output contract

Print exactly this structure to chat. No lengthy preamble — open directly with the variants.

```
---

**Variant A — שאלת כאב**

[Full Hebrew post, RTL, link as last line]

---

**Variant B — תובנה קונקרטית**

[Full Hebrew post, RTL, link as last line]

---

**Variant C — סיפור / ציטוט**

[Full Hebrew post, RTL, link as last line]

---

> **המלצה:** [One Hebrew sentence: which variant fits this article best and why.]

**לפני הפרסום:**
- [ ] הדביקו את הקישור ובדקו שתצוגת התקדים (תמונה + כותרת) נטענת תקין. אם לא — בדקו את תגיות ה-OG של העמוד לפני הפרסום.
- [ ] אחרי שהתצוגה המקדימה נטענה, אפשר למחוק את שורת ה-URL הגולמית מגוף הפוסט — הכרטיס נשאר.
- [ ] פרסמו כשהקהל ער: לקהל מנהלים בישראל, בדרך כלל ימים א׳–ה׳ בבוקר (7:30–9:00) או בערב (20:30–22:00). בדקו מול נתוני העמוד שלכם אם יש.
- [ ] הישארו זמינים כ-30–60 דקות אחרי הפרסום — תגובה מהירה לתגובות מכפילה את התפוצה.
- [ ] אל תפרסמו קישור נוסף באותו יום מאותו עמוד. כתבה אחת = פוסט אחד; אפשר זווית שנייה אחרי שבוע-שבועיים.
```

## 7. Quality checks before outputting

- Every hook line is ≤ ~110 characters and works with nothing after it.
- No variant restates the article's title verbatim (the link card shows it).
- Every fact, quote, and scene traces back to the article or `kidma-plugins:overview` — nothing invented.
- No engagement bait, no clickbait withholding, no hype words, ≤ 1 emoji, ≤ 2 hashtags.
- Each full post is 300–600 Hebrew characters (hard cap ~800), with line breaks between thoughts.
- The bridge line names what the reader gets in the article, not a generic "read more".
- A reader who never clicks still walked away with one true, useful thing.

## 8. When to stop and ask

Stop generating and ask the human if:

- There is no published URL yet — offer to draft anyway but flag that the link line will be a placeholder.
- The article content isn't available and can't be fetched — never write from a title alone.
- The strongest hook would require a statistic, quote, or school name that the article doesn't actually contain.
- The human asks for tactics this skill deliberately avoids (engagement bait, tagging people for reach, posting the same link across many groups) — explain briefly why they backfire and offer the compliant alternative.

## 9. Example output

Given the example article from `write-article` («שלוש שאלות לשאול לפני כל פיילוט AI בבית הספר», published at `https://kid-ma.com/articles/three-pilot-questions`):

---

**Variant A — שאלת כאב**

עוד הצעה לפיילוט AI נחתה לכם על השולחן. איך יודעים אם לומר כן?

מנהלות מנוסות שעובדות איתנו לא מתחילות מהכלי. הן מתחילות משלוש שאלות — רבע שעה שמסננת מראש את רוב הבעיות שצצות אחרי חודשיים.

בכתבה: שלוש השאלות, ולמה דווקא השנייה מפילה את רוב הפיילוטים.

https://kid-ma.com/articles/three-pilot-questions

---

**Variant B — תובנה קונקרטית**

רבע שעה של שאלות לפני פיילוט AI חוסכת חודשים של כיבוי שריפות אחריו.

זה הדפוס שראינו שוב ושוב בבתי ספר: הפיילוטים שנכשלים לא נכשלים בגלל הכלי — הם נכשלים בגלל שאלות שאף אחד לא שאל בהתחלה.

בכתבה החדשה ריכזנו את שלוש השאלות ששווה לשאול לפני שאומרים כן.

https://kid-ma.com/articles/three-pilot-questions

---

**Variant C — סיפור / ציטוט**

"לפני שאני שומעת הדגמה, אני שואלת שלוש שאלות." כך פתחה איתנו מנהלת חטיבת ביניים את שיחת הפיילוט הראשונה.

השאלות שלה היו כל כך מדויקות שהפכנו אותן לחלק מהתהליך עם כל בית ספר חדש.

מה הן — ולמה הן עובדות — בכתבה המלאה:

https://kid-ma.com/articles/three-pilot-questions

---

> **המלצה:** לכתבה פרקטית עם מסגרת פעולה ברורה, Variant A פונה הכי ישירות לרגע ההחלטה של המנהלת; אם הפוסט הקודם בעמוד היה שאלה, גוונו עם C.

---

## Related Skills

- **`kidma-plugins:write-article`** — Produces the article this skill promotes. Its `excerpt` frontmatter usually feeds the OG description shown in the link card — avoid repeating it in the post body.
- **`kidma-plugins:article-image-prompt`** — Generates the article's hero image, which becomes the link-preview image this post relies on.
- **`kidma-plugins:overview`** — Required. Audience definition and verifiable company facts.
- **`kidma-plugins:brand`** — Required. Slogan formatting and tone principles.
