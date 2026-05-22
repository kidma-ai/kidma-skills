# ⚡ Kidma Plugin Marketplace

> Official Kidma plugin library for **Claude Code** — lesson planning, presentations, and brand assets.

## Quick Start

```bash
# Add the marketplace (replace YOUR_ORG with your GitHub org/user)
/plugin marketplace add YOUR_ORG/kidma-skills

# Install all foundation plugins (required by other plugins)
/plugin install kidma-company-overview@kidma-plugins
/plugin install kidma-brand-guidelines@kidma-plugins

# Install lesson planning plugins
/plugin install kidma-lesson-generator@kidma-plugins
/plugin install kidma-lesson-docx@kidma-plugins

# Use a skill
/kidma-lesson-generator:kidma-lesson-generator
```

---

## Available Plugins

### 🏢 Foundation — install these first

| Plugin | Description |
|--------|-------------|
| `kidma-company-overview` | Full Kidma company context — programs, metrics, history |
| `kidma-brand-guidelines` | Official brand styling — colors, typography, logos, assets |

### 📚 Lessons

| Plugin | Description |
|--------|-------------|
| `kidma-lesson-generator` | Generate complete lesson plans (Understand → Try → Create) |
| `kidma-lesson-docx` | Export lesson plan to branded Word document |
| `kidma-lesson-extractor` | Extract content from existing Kidma lesson materials |
| `kidma-lesson-summary` | Generate PDF lesson summary for students |

### 🎨 Presentations

| Plugin | Description |
|--------|-------------|
| `kidma-presentation-planner` | Plan slides interactively with step-by-step approval |
| `kidma-presentation-builder` | Build PPTX file from an approved slide plan |

---

## Recommended Pipelines

**New lesson → Word doc:**
```
kidma-lesson-generator  →  kidma-lesson-docx
```

**New presentation:**
```
kidma-presentation-planner  →  kidma-presentation-builder
```

---

## Team Setup — Auto-install via project settings

Add this to `.claude/settings.json` in your project so the marketplace is available to everyone on the team automatically:

```json
{
  "extraKnownMarketplaces": {
    "kidma-plugins": {
      "source": {
        "source": "github",
        "repo": "YOUR_ORG/kidma-skills"
      }
    }
  },
  "enabledPlugins": {
    "kidma-company-overview@kidma-plugins": true,
    "kidma-brand-guidelines@kidma-plugins": true,
    "kidma-lesson-generator@kidma-plugins": true,
    "kidma-lesson-docx@kidma-plugins": true,
    "kidma-presentation-planner@kidma-plugins": true,
    "kidma-presentation-builder@kidma-plugins": true
  }
}
```

---

## Repository Structure

```
kidma-skills/
├── .claude-plugin/
│   └── marketplace.json              ← Marketplace catalog (required)
├── plugins/
│   ├── kidma-company-overview/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/kidma-company-overview/SKILL.md
│   │   └── references/full-context.md
│   ├── kidma-brand-guidelines/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/kidma-brand-guidelines/SKILL.md
│   │   └── assets/logo_*.png
│   ├── kidma-lesson-generator/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/kidma-lesson-generator/SKILL.md
│   │   └── references/deep-dive.md
│   ├── kidma-lesson-docx/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/kidma-lesson-docx/SKILL.md
│   │   ├── assets/template.docx
│   │   └── scripts/build_lesson.py
│   ├── kidma-lesson-extractor/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/kidma-lesson-extractor/SKILL.md
│   │   └── references/output-template.md
│   ├── kidma-lesson-summary/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/kidma-lesson-summary/SKILL.md
│   ├── kidma-presentation-planner/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/kidma-presentation-planner/SKILL.md
│   │   └── references/slide-types.md
│   └── kidma-presentation-builder/
│       ├── .claude-plugin/plugin.json
│       ├── skills/kidma-presentation-builder/SKILL.md
│       ├── assets/template.pptx
│       └── references/slide-catalog.md
└── README.md
```

---

## Releasing Updates

1. Edit the plugin files
2. Bump `"version"` in the plugin's `.claude-plugin/plugin.json`
3. Push to GitHub

Users update with:
```bash
/plugin marketplace update kidma-plugins
```

---

## Contact

Kidma Technologies and Education Ltd. | kidma2030@gmail.com | [kid-ma.com](https://kid-ma.com)
