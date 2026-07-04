# kidev

Developer git workflow automation for Claude Code.

| Skill          | What it does                                                                                          |
|----------------|--------------------------------------------------------------------------------------------------------|
| `publish_code` | Full save-and-ship cycle — branch, commit, push, open a PR, merge it (squash), then back to main + pull. |

## Usage

Trigger with phrases like "save", "save changes", "publish code", "ship this", or "push and merge". The skill scopes the commit to files touched in the current session (falling back to `git status` if none), asks for confirmation on the branch name and commit message via `AskUserQuestion`, then runs the full cycle through to a merged `main`.
