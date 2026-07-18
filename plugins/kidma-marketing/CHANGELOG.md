# Changelog — kidma-marketing

## 1.4.0 — 2026-07-18

- `kidma-daily-scan` gains competitor intelligence. Bundles a new `references/competitors.md` (threat tiers, dated facts tagged עובדה/הערכה/הסקה, Kidma's Gefen position and differentiators, competitor-watch source list, and reliability caveats). Adds a `COMPETITOR` scenario ("competitor" / "סריקת מתחרים"), a sixth relevance-lens category for competitor moves (funding, acquisitions, Gefen listings, Hebrew localization, Ministry integrations, launches/shutdowns), and a new dossier section 6 "מודיעין תחרותי" (renumbering זרעי כתבות → 7 and הערות תפעול → 8). Article seeds now carry a differentiation note, and failure rules require competitor facts to keep their original tag/date and be re-verified when older than ~6 months.

## 1.3.0 — 2026-07-18

- New skill: `kidma-daily-scan` — runs Kidma's content-source scan across the AI-in-education source catalog (Hebrew/English media, creators, institutional research, journals) and produces a self-contained Hebrew context dossier rich enough to feed `write-article`, `facebook-post`, Instagram, and newsletter work without re-research. Picks a scenario by day of week or explicit request, filters through the Kidma relevance lens, harvests audience-ready practical tips, and archives dated dossiers when a project folder is available. Designed to run autonomously inside a Claude routine. Bundles `references/sources.md` (source catalog) and `references/calendar.md` (weekly cadence, annual calendar, channel mapping).

## 1.2.1 — 2026-07-08

- `write-article` refined for the promotion stage: articles must leave promotion hooks in the prose (a concrete observation + a quotable field moment) for `facebook-post` to mine; `heroDescription` now written for the 1200×630 social link-preview crop; `title` front-loads meaning within the ~60-char social truncation; `excerpt` explicitly serves as the link-preview description (add a reason to read, don't restate the title). Related Skills updated to reference `facebook-post`.

## 1.2.0 — 2026-07-08

- New skill: `facebook-post` — writes three Hebrew Facebook post variants (pain-point question / concrete insight / story-quote hooks) promoting a published kid-ma.com article, with a publishing checklist (link preview, timing, comment follow-up). Built on current organic-reach best practices: value-first copy, above-the-fold hooks, no engagement bait or clickbait.

## 1.0.0 — 2026-06-05

- Initial release — `write-article` skill added (Hebrew article drafting for kid-ma.com, newsletters, and school proposals)
