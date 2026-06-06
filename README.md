# ⚡ Kidma Plugin Marketplace

> Official Kidma plugin library for **Claude Code** — lesson planning, presentations, brand assets, and content drafting in Hebrew.

## Quick Start

```bash
# Add the marketplace
/plugin marketplace add kidma-ai/kidma-skills

# Install the foundation plugin (required by the other two)
/plugin install kidma-company@kidma-plugins

# Install the plugins you want
/plugin install kidma-pedagogy@kidma-plugins
/plugin install kidma-marketing@kidma-plugins
/plugin install kidma-media@kidma-plugins

# Invoke a skill
/kidma-pedagogy:lesson-planner
```

---

## Plugins

Four domain plugins, seventeen skills total.

### 🏢 `kidma-company` — foundation, install first

Reference skills used as context by every other plugin.

| Skill | Purpose |
|-------|---------|
| `overview` | Full Kidma company context — programs, audience, partners, vision |
| `brand` | Brand styling — colors, typography, logos, methodology code |

### 📚 `kidma-pedagogy` — lesson + presentation authoring

| Skill | Purpose |
|-------|---------|
| `lesson-planner` | Interactively plan a Kidma lesson plan (Understand → Try → Create), output structured JSON |
| `lesson-to-word` | Build a branded `.docx` from the planner's JSON |
| `lesson-exercise` | Build a student exercise/summary `.pdf` from the planner's JSON |
| `slides-planner` | Interactively plan a slide deck for a Kidma lesson, output approved slide list |
| `slides-builder` | Build the branded `.pptx` from the approved slide plan |
| `structure-lesson-content` | Extract and structure content from existing Kidma lesson materials |

### ✍️ `kidma-marketing` — Hebrew article authoring

| Skill | Purpose |
|-------|---------|
| `write-article` | Draft a complete Hebrew article (frontmatter + Markdown body) for kid-ma.com, newsletters, or school proposals |
| `article-image-prompt` | Generate Nano Banana image prompts (documentary + conceptual styles) for an article |

### 🎨 `kidma-media` — Gemini image, video, and audio generation

Requires `GEMINI_API_KEY`. Run `setup` once before the action skills.

| Skill | Purpose |
|-------|---------|
| `setup` | One-time setup — checks Python deps, `GEMINI_API_KEY`, output dir, and pings the API |
| `generate-image` | Generate an image via Nano Banana 2 or Imagen 4, with Kidma brand presets |
| `edit-image` | Edit an existing image with a natural-language instruction (Nano Banana 2) |
| `describe-image` | Describe / OCR / caption an image via Gemini multimodal (Hebrew RTL preserved) |
| `generate-video` | Generate a short (≤8s) video via Veo 3 — text-to-video or image-to-video |
| `tts` | Synthesize Hebrew (or any language) speech via Gemini TTS — 24 kHz mono WAV |
| `refresh-models` | Refresh `assets/models.yaml` against the live Gemini docs MCP server |

---

## Bundles (recommended pipelines)

The marketplace defines named bundles that chain skills end-to-end. See `.claude-plugin/marketplace.json` for the full spec.

| Bundle | Flow |
|--------|------|
| `kidma-lesson-full` | `lesson-planner` → `lesson-to-word` → `lesson-exercise` — blank topic to branded `.docx` + student exercise `.pdf` |
| `kidma-presentation-full` | `slides-planner` → `slides-builder` — lesson content to branded `.pptx` |
| `kidma-article-full` | `write-article` → `article-image-prompt` — topic brief to article draft + matching image prompts |

**Article publishing:** `write-article` produces an `.md` block in chat. To publish to kid-ma.com, the project-local `publish-article` skill in the `kidma-site` repo picks it up and turns it into an MDX file + PR.

---

## Team Setup — auto-install via project settings

Add this to `.claude/settings.json` in your project so everyone on the team gets the marketplace and the plugins automatically:

```json
{
  "extraKnownMarketplaces": {
    "kidma-plugins": {
      "source": {
        "source": "github",
        "repo": "kidma-ai/kidma-skills"
      }
    }
  },
  "enabledPlugins": {
    "kidma-company@kidma-plugins": true,
    "kidma-pedagogy@kidma-plugins": true,
    "kidma-marketing@kidma-plugins": true,
    "kidma-media@kidma-plugins": true
  }
}
```

---

## Repository structure

```
kidma-skills/
├── .claude-plugin/
│   └── marketplace.json              ← Catalog + bundle definitions
├── plugins/
│   ├── kidma-company/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/
│   │   │   ├── overview/SKILL.md
│   │   │   └── brand/SKILL.md
│   │   ├── references/full-context.md
│   │   └── assets/logo_*.png
│   ├── kidma-pedagogy/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/
│   │   │   ├── lesson-planner/SKILL.md
│   │   │   ├── lesson-to-word/SKILL.md
│   │   │   ├── lesson-exercise/SKILL.md
│   │   │   ├── slides-planner/SKILL.md
│   │   │   ├── slides-builder/SKILL.md
│   │   │   └── structure-lesson-content/SKILL.md
│   │   ├── references/
│   │   ├── schemas/
│   │   ├── scripts/build_lesson.py
│   │   └── assets/{template.docx, template.pptx}
│   ├── kidma-marketing/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/
│   │       ├── write-article/SKILL.md
│   │       └── article-image-prompt/SKILL.md
│   └── kidma-media/
│       ├── .claude-plugin/plugin.json
│       ├── skills/
│       │   ├── setup/SKILL.md
│       │   ├── generate-image/SKILL.md
│       │   ├── edit-image/SKILL.md
│       │   ├── describe-image/SKILL.md
│       │   ├── generate-video/SKILL.md
│       │   ├── tts/SKILL.md
│       │   └── refresh-models/SKILL.md
│       ├── scripts/
│       └── assets/models.yaml
├── CLAUDE.md
└── README.md
```

---

## Releasing updates

1. Edit the plugin / skill files.
2. Bump `"version"` in the relevant `plugins/<name>/.claude-plugin/plugin.json` and add an entry to the plugin's `CHANGELOG.md`.
3. If the marketplace surface changes (new plugin, renamed plugin, new bundle), also bump `"version"` in `.claude-plugin/marketplace.json`.
4. Validate: `python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"` and `claude plugin validate plugins/<name>/`.
5. Push to GitHub.

Users update with:

```bash
/plugin marketplace update kidma-plugins
```

---

## Contact

Kidma Technologies and Education Ltd. | kidma2030@gmail.com | [kid-ma.com](https://kid-ma.com)
