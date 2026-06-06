# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **Claude Code plugin marketplace** (not an app). It publishes skills that other Claude Code users install via `/plugin marketplace add`. There is no build step, no test suite, and no runtime — the "code" is markdown skill definitions plus a few Python scripts that skills shell out to.

## Architecture

Three layers, top-down:

1. **`.claude-plugin/marketplace.json`** — the catalog. Lists the plugins exposed by this repo and defines `bundles` (named pipelines that chain skills across plugins, e.g. `kidma-lesson-full`: `lesson-planner` → `lesson-to-word` → `lesson-exercise`).
2. **`plugins/<plugin-name>/.claude-plugin/plugin.json`** — one per plugin. **Must conform to Claude Code's plugin manifest schema** (`name`, `version`, `description`, `author`, `homepage`, `repository`, `keywords`). Validate with `claude plugin validate plugins/<name>/`. Don't add custom fields like `dependencies` (object form), `skills` (array form), `category`, `tags`, `changelog`, or `$schema` — the live validator rejects them even though the public docs hint otherwise. Per-plugin `CHANGELOG.md` lives at the plugin root instead.
3. **`plugins/<plugin-name>/skills/<skill>/SKILL.md`** — the actual skill. Must be a directory containing `SKILL.md`; flat `skills/<skill>.md` files are not discovered. YAML frontmatter (`description`, plus repo-internal hints like `type`, `depends_on`, `invokes`, `input_*`/`output_*` which are documentation only) followed by the prompt body that Claude follows when the skill is invoked. Inside a skill, refer to plugin-root resources via `${CLAUDE_PLUGIN_ROOT}/assets/...`, `${CLAUDE_PLUGIN_ROOT}/scripts/...`, etc. — never relative paths, since the skill now lives one level deeper than the plugin root.

Current plugin set (3 domain plugins, restructured in commit `c039e89` from 8 micro-plugins — **the README still describes the old 8-plugin layout and is stale**):

- `kidma-company` — foundation. `overview` + `brand` reference skills. Required by both other plugins.
- `kidma-pedagogy` — lesson + presentation authoring. 6 skills forming two pipelines (lesson and slides).
- `kidma-marketing` — Hebrew article drafting + image-prompt generation.

### Skill pipeline convention

Skills hand off via well-known file paths, not function calls. A planner/interactive skill writes its structured output to `/home/claude/<artifact>.json|.txt`; a generation skill reads from there and writes the final file to `/mnt/user-data/outputs/<file>.<ext>`. The `input_file` / `output_file` fields in each skill's frontmatter (and the bundle `pipeline` entries in `marketplace.json`) document this contract — when adding or editing a skill that participates in a pipeline, keep those paths consistent across both ends.

### `depends_on` semantics

`depends_on: [kidma-plugins:overview, kidma-plugins:brand]` in a skill's frontmatter means **read those skills at session start before generating output**. It is a content/context dependency, not a runtime import. Every content-producing skill depends on the `kidma-company` foundation skills.

### Python helpers

`plugins/kidma-pedagogy/scripts/build_lesson.py` (and the equivalent for pptx) are invoked by the matching skill via `bash` — they're declared in the skill's `runtime` block (`tools: [bash]`, `python_packages: [python-docx]`). They unpack a branded `.docx`/`.pptx` template from `assets/`, rebuild the document XML body from the JSON content, and repack — preserving headers, footers, logos, and Hebrew RTL styling. Schemas for the JSON contracts live in `plugins/kidma-pedagogy/schemas/`.

## Hebrew / RTL

Output is Hebrew, right-to-left. The DOCX/PPTX templates encode RTL paragraph properties (`<w:rtl w:val="1"/>`) and the Rubik font. Don't strip or override these when editing the build scripts.

## Releasing

1. Edit the plugin/skill files.
2. Bump `version` in the relevant `plugins/<name>/.claude-plugin/plugin.json` and add a `changelog` entry.
3. If the change affects the marketplace surface (new plugin, renamed plugin), also bump `version` in `.claude-plugin/marketplace.json`.
4. Commit and push. Users pull via `/plugin marketplace update kidma-plugins`.

No CI runs on this repo. Validation is "does the JSON parse and does the skill behave when installed."

## Notes for editing

- `README.md` documents the **old** 8-plugin structure (`kidma-lesson-generator`, `kidma-presentation-planner`, etc.). The real plugins are the 3 in `plugins/`. Update the README opportunistically when touching nearby content; don't trust it as a source of truth.
- `marketplace.json` must be strict JSON — Claude Code's marketplace parser rejects trailing commas. Validate with `python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"` before pushing.
- Skill `description` fields are long and trigger-rich on purpose: Claude Code uses them to decide when to invoke the skill, so keep them keyword-dense and include the Hebrew phrasings (`מערך שיעור`, `מצגת`) that users actually type.