---
description: "Full save-and-ship cycle: create a feature branch, stage + commit all changes, push, open a PR, merge it, then return to main and pull. One command to go from dirty working tree to merged main. Use when you want to save and ship the current changes without manually managing git. Triggers: 'save', 'save changes', 'publish code', 'commit and merge', 'ship this', 'push and merge', 'save and push'."
---

# Publish Code — Branch · Commit · Push · PR · Merge · Back to Main

Full cycle: dirty working tree → merged main. Runs in order; stops and surfaces any failure before moving to the next step.

## 0. Determine session files (when running mid-session)

**If this skill is invoked during an active Claude Code session** (i.e., the current conversation already contains tool calls where Claude edited or wrote files), identify those files from the session context before doing anything else:

- Scan the current conversation for all `Edit`, `Write`, and `NotebookEdit` tool calls made during this session. Collect every distinct file path that was touched.
- This is the **session file list** — it takes priority over a blind `git status` sweep when deciding what to stage.
- Cross-reference against `git status` to confirm the files are actually dirty (they should be). Ignore session-listed files that are already clean.
- If the session file list is empty (skill was invoked with no prior edits in the conversation), fall back to `git status` to discover what's modified.

This ensures the commit is scoped to what this session actually changed, not to unrelated dirty files that happened to be present.

## 1. Sanity checks

Before touching git:

- Run `git status` — if the tree is clean (nothing staged, nothing modified, no untracked files relevant to the work), tell the human "Nothing to save — working tree is clean." and stop.
- Confirm the current branch is `main`. If not, warn: "You're on branch `<name>`, not main. Proceed anyway?" Wait for explicit yes before continuing.

## 2. Branch name

Use the session file list (§0) and `git diff HEAD -- <session-files>` to understand what changed.

Propose a short kebab-case feature branch name that describes the change (2–4 words). Format: `feat/<name>`, `fix/<name>`, or `chore/<name>` as appropriate.

Use the `AskUserQuestion` tool to ask for the branch name. Offer the proposed name as the first option, plus an "Other" option so the human can type a custom name:

```
question: "What should the branch name be?"
header: "Branch name"
options: [
  { label: "<proposed-branch-name>", description: "(Recommended)" },
  { label: "Other", description: "Type a custom branch name" }
]
```

Use whatever the human selects or types. If they select the recommended option, use the proposed name.

## 3. Create and check out the branch

```bash
git checkout -b <branch-name>
```

## 4. Stage and commit

Stage the **session file list** from §0 (or all relevant dirty files if no session list). Don't blindly `git add .` — never stage files that weren't part of this session's work, and always skip `.env`, build artifacts, and accidental lock-file changes.

Draft a commit message:
- Subject line: ≤72 chars, imperative mood, describes *what* changed.
- No body needed unless the change is complex.

Use the `AskUserQuestion` tool to confirm or override the commit message before committing:

```
question: "What should the commit message be?"
header: "Commit message"
options: [
  { label: "<proposed-commit-message>", description: "(Recommended)" },
  { label: "Other", description: "Type a custom commit message" }
]
```

Use whatever the human selects or types. Then commit:

```bash
git commit -m "<message>

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

## 5. Push

```bash
git push -u origin <branch-name>
```

## 6. Open a PR

```bash
gh pr create \
  --title "<commit subject>" \
  --body "$(cat <<'EOF'
## Summary
<1–3 bullet points describing the change>

## Test plan
- [ ] Visual check on affected pages
- [ ] No lint / build errors

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Print the PR URL.

## 7. Merge the PR

Wait ~3 seconds for GitHub to register the PR, then:

```bash
gh pr merge <pr-number-or-url> --squash --delete-branch
```

Use `--squash` to keep the main history clean. If the repo has branch-protection rules that require reviews or CI to pass, this will fail — surface the error and tell the human: "PR is open but can't auto-merge. Merge manually when ready." Then skip to §8 anyway (checkout + pull).

## 8. Return to main and pull

```bash
git checkout main
git pull
```

Confirm the merge is visible:

```bash
git log --oneline -3
```

Print the top 3 lines so the human can see their commit landed.

## 9. Done

One-line confirmation: "Saved. `<branch-name>` is merged into main."

---

## Error handling

| Failure point | What to do |
|---|---|
| Branch name already exists | Append `-2` and try once; if still taken, ask the human. |
| Commit hook fails | Report the hook output. Fix the underlying issue (lint, type error) before retrying. Never use `--no-verify`. |
| Push rejected | Show the error. Most likely a remote branch conflict — don't force-push without explicit human instruction. |
| PR creation fails | Print the `gh` error. Offer the manual `gh pr create` command so the human can run it themselves. |
| Merge blocked by branch protection | Announce the PR URL and tell the human to merge manually. Still run §8. |
