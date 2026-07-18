---
name: kidma-daily-scan
description: >
  Run Kidma's content-source scan and produce a raw, self-contained context dossier
  for the marketing pipeline. ALWAYS use this skill when a scheduled task / routine
  says "run the daily scan", "kidma daily scan", "scan the sources", "content digest",
  "סריקת מקורות", or "דוח תוכן" — and also for on-demand runs like "run the Hebrew tier",
  "scan the weekly tier", "full scan", "scan [source name]", "scan for [topic]",
  "run the competitor scan" / "סריקת מתחרים", or when the user asks what's new in
  AI-in-education sources for Kidma content. The skill picks the scenario (by day of
  week or explicit request), filters items through the Kidma lens, flags competitor
  moves against bundled competitor intelligence, extracts audience-ready tips, and
  outputs a complete dossier. No Notion or external services: with a Cowork project
  folder the dossier is also saved as a dated .md file (enabling dedupe); otherwise
  output only. Runs autonomously — never pause to ask questions mid-run.
---

# Kidma Source Scan → Raw Context Dossier

Scans AI-in-education sources and produces one output: a **self-contained dossier**
rich enough that a later session can write the blog article, Facebook posts, Instagram
content, and newsletter section from it **without any re-research**. The dossier is the
only artifact — nothing is saved to Notion or any external store.

**Runs unattended.** Never ask clarifying questions. Degrade gracefully (see Failure Rules).

## Step 0 — Load references

Read all three reference files before scanning:
- `references/sources.md` — the full source catalog (tiers, URLs, what each gives Kidma).
- `references/calendar.md` — weekly cadence, annual calendar, channel mapping.
- `references/competitors.md` — competitor intelligence: threat tiers, dated facts with
  their fact/estimate/inference tags, Kidma differentiators, and the competitor-watch
  source list. Applies to EVERY scenario, not only competitor scans.

## Step 1 — Pick the scenario

**Explicit request wins.** If the invoking prompt names a scenario, run it:

| Request contains | Scenario | Sources (from sources.md) | Window |
|---|---|---|---|
| "hebrew" / "עברית" / "Hebrew tier" | HEBREW | All HE DAILY sources | last 48h (or stated window) |
| "english" / "English tier" | ENGLISH | All EN DAILY sources (media + creators) | last 48h |
| "weekly" | WEEKLY | All WEEKLY sources, EN + HE | last 7 days |
| "monthly" / "company" | MONTHLY | Company blogs + MONTHLY sources | last 30 days |
| "quarterly" / "reports" / "journals" | REPORTS | Institutional + journals | last 90 days |
| "full" / "everything" | FULL | DAILY + WEEKLY, EN + HE | last 7 days |
| "scan [source name]" | SINGLE | That source only, deep read of recent items | last 30 days |
| "scan for [topic]" | TOPIC | web_search + best-matching catalog sources | last 30 days |
| "competitor" / "מתחרים" | COMPETITOR | Competitor-watch sources in competitors.md | last 30 days |

A stated time window in the request ("last two weeks") overrides the default window.

**No explicit scenario** (plain "run the daily scan") → choose by day of week:
Sunday = HEBREW · Mon–Thu = ENGLISH · Friday = WEEKLY · Saturday = no run
(output "No scan on Saturday" and stop, unless a scenario was explicitly requested).

## Step 2 — Scan

For each source: web_fetch its main/news page; if fetch fails or the site is JS-heavy,
fall back to web_search scoped to the source and the current month/year. Respect the
scenario's recency window strictly — an item's publication date must fall inside it.

## Step 3 — Relevance filter (Kidma lens)

Keep an item only if it clearly touches at least one:
1. **AI in K-12 schools** — adoption, tools, national programs, classroom practice.
2. **Teacher / principal psychology** — trust, resistance, mindset shift, training, self-efficacy.
3. **AI tutors & pedagogical agents** — results, debates, failures, multi-agent learning (Kidma's 2028 vision).
4. **Israel** — Ministry of Education, Israeli edtech, Hebrew discourse.
5. **AI literacy & assessment** — competency frameworks, "how do we know a student learned".
6. **Competitor moves** — any item involving an entity in competitors.md: funding,
   acquisitions, new Gefen listings, Hebrew localization, Ministry integrations,
   school wins, product launches or shutdowns/failures.

Discard higher-ed-only admin news, model releases with no education angle, and hollow
vendor PR. Target the 3–6 strongest items (SINGLE/TOPIC scans may keep more).

## Step 4 — The dossier (the only output)

Written in **Hebrew (RTL)**; quotes stay in their original language. Dense and factual —
this is working material, not a newsletter. Structure:

```
# דוסייה סריקת מקורות — [scenario] — [scan date]

## 1. מטא
Scenario, window, sources scanned successfully, sources failed (with reason).

## 2. תמונת מצב
3–5 sentences: what is happening in the field right now based on today's items,
including tensions/disagreements between sources.

## 3. פריטים
For EACH kept item, all of the following:
- **מקור + תאריך פרסום + URL מלא**
- **סיכום עובדתי** — 4–8 sentences, dense paraphrase: the claims, the numbers,
  the named people/orgs, the context. Enough that the article can be written
  without opening the link.
- **נתונים ומספרים** — every stat in the item, each with its original source
  attribution as stated in the item.
- **ציטוט** — at most ONE short quotable phrase (<15 words, original language,
  attributed). If exact wording is uncertain — paraphrase only, marked as such.
- **סיווג** — fact / estimate / opinion, per claim where they differ.
- **רלוונטיות לקידמה** — which of the 5 lens categories, and the specific hook
  (product / pedagogy / sales / vision).
- **זויות לערוצים** — one line each: blog angle · FB hook · IG visual idea ·
  newsletter framing (per references/calendar.md channel mapping).

## 4. טיפ ישים לקהל
1–2 practical quick-wins harvested from today's items: a small trick, prompt
technique, tool feature, or classroom/leadership practice a teacher or principal
can apply TODAY in under 10 minutes. Each tip: what to do (2–3 concrete steps) ·
who it serves (teacher / principal / parent) · source item it came from ·
one-line FB/IG micro-post phrasing. Only include tips actually grounded in a
scanned item — if today's items yield none, write "אין טיפ מבוסס-מקור היום"
rather than inventing one.

## 5. חיבורים
Cross-item synthesis: shared themes, contradictions to address honestly,
ties to the annual-calendar moment of the current month (from calendar.md),
and Ministry-vocabulary hooks (בינה מלאכותית לכל, כשירות AI) where natural.

## 6. מודיעין תחרותי
Competitor-relevant items from this window (category 6 of the lens), each with:
what happened (dated, tagged עובדה/הערכה/הסקה per competitors.md conventions) ·
threat-tier of the entity · what it changes for Kidma's positioning, pricing (Gefen),
or the אור differentiator · suggested response angle if any. If nothing surfaced:
"לא זוהו מהלכי מתחרים בחלון הסריקה" — never pad this section.

## 7. זרעי כתבות
2–3 concrete article seeds. Each: working title (HE) · thesis in one sentence ·
which dossier items support it · suggested מבינים/מנסים/יוצרים framing ·
which skeptic/counter-voice to engage for credibility · differentiation note —
where the angle occupies ground competitors miss (per competitors.md: the
psychology/mindset lane, Hebrew-first pedagogy, responsible-AI/failure lessons,
platform+continuity). Standing content opportunities in competitors.md may seed
an article when today's items connect to them — but only with a fresh hook.

## 8. הערות תפעול
Failed sources, items needing manual verification, conflicts left unresolved.
```

## Step 5 — Archive (file-based, no external services)

If the session has a writable project working folder (a Cowork project):
1. Ensure a `dossiers/` subfolder exists in the project folder.
2. Save the full dossier there as `YYYY-MM-DD-[scenario].md` (e.g., `2026-07-19-hebrew.md`).
3. Before writing (back in Step 2–3), read the dossier files whose dates fall inside
   the current scenario window and use them for dedupe.
4. The chat/task output should still contain the full dossier — the file is the
   archive, not a replacement for delivering the result.

If no writable persistent folder is available (plain chat or a routine without a
project folder): skip archiving silently and deliver the dossier as output only.
Never use Notion or any external storage service.

## Failure Rules

- A failed source: skip, note in section 8, continue. One source never kills the run.
- Fewer than 3 relevant items: report honestly what exists. Never pad, never invent.
- Never fabricate quotes, stats, dates, or attributions. Uncertain wording → paraphrase.
- All item dates are publication dates, not the scan date.
- Competitor facts cited from competitors.md keep their original tag and date
  (עובדה/הערכה/הסקה); re-verify before presenting any of them as current if the
  fact is older than ~6 months. Reliability caveats listed there travel with the fact.
- Conflicting sources: include both sides and flag the conflict in sections 3 and 5.
- Dedupe: if a dossier archive folder exists (see Archive step), read the dossiers
  from the current window before writing, and drop items already covered unless there
  is a genuine update (then mark it "עדכון ל..."). With no archive available, the
  recency window is the only dedupe — flag likely repeats rather than hide them.

## Manual invocation

Same flow when a user asks mid-conversation; follow-up questions are then allowed,
and the user may narrow the dossier ("only section 7", "English output").
