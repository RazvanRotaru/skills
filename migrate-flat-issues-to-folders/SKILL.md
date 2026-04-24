---
name: migrate-flat-issues-to-folders
description: One-shot migration of a vault project from flat issue files (vault/projects/<Project>/issues/<slug>.md) to per-issue folders (vault/projects/<Project>/issues/<slug>/issue.md). Rewrites board wiki-links, adds missing priority tags, and updates issue-note frontmatter. Idempotent. Use when retrofitting an existing vault to the Obsidian-kanban-orchestration layout.
---

# Migrate Flat Issues to Folders

One-shot migration for vault projects predating the per-issue-folder layout. Walks `vault/projects/<Project>/issues/`, converts flat `<slug>.md` files into `<slug>/issue.md`, rewrites `board.md` wiki-links, and backfills missing frontmatter fields.

## When to use

- The project's issues live as flat files at `vault/projects/<Project>/issues/<slug>.md` and the new orchestration layout (folders with `issue.md` + `progress/`) is needed.
- You see flat-file wiki-links in `board.md` like `- [ ] [[issues/<slug>]] #AFK` that need updating.

**Not for:** projects already on the new layout — the skill will detect that and exit cleanly.

## Inputs

- **Project name** — the `<Project>` segment under `vault/projects/`.
- **Vault path** — resolved from `./vault/` in the workspace root. User may override.

## What the skill does

### Per flat issue file

For each `vault/projects/<Project>/issues/*.md` that is a flat file (not a folder):

1. **Derive slug.** `<slug>` = filename stem, slugified:
   - Lowercase.
   - Spaces → hyphens.
   - Strip punctuation other than `-`.
   - Collapse repeated hyphens.
2. **Check for collision.** If `issues/<slug>/` already exists, skip this file and warn — requires manual resolution.
3. **Create the folder.** `mkdir -p issues/<slug>/`.
4. **Move the file.** `mv issues/<original-filename>.md issues/<slug>/issue.md`.
5. **Backfill frontmatter.** Open `issue.md`, add any of these missing fields:
   - `priority: P1` — default if not present.
   - `scope: ""` — empty string as a prompt for the user to fill in later.
   - `branch: null` — populated by orchestrator later.

### Board wiki-link rewrites

Open `vault/projects/<Project>/board.md`. For every checklist line matching a flat-file pattern:

- `- [ ] [[issues/<original>]] <tags>` → `- [ ] [[issues/<slug>/issue|<slug>]] <tags>`
- If `<tags>` lacks any `#P0`/`#P1`/`#P2` tag, insert `#P1` before the first existing tag (or at end if none).

Preserve the `kanban-plugin: board` frontmatter and column headers byte-for-byte. Only checklist lines change.

### Issue cross-references

If moved `issue.md` files contain wiki-links to other issues in the `[[issues/<other-slug>]]` flat-file form, rewrite them to `[[issues/<other-slug>/issue]]`.

## Process

1. **Sanity checks.**
   - Vault path exists.
   - `vault/projects/<Project>/` exists and contains `issues/` and `board.md`.
   - If not, tell the user they likely need to run `init-obsidian-kanban-project` first.

2. **Discover.** Walk `issues/`. Separate flat files from existing folders.
   - If all entries are folders: print "already migrated" and exit cleanly.
   - If some are flat and some are folders: proceed, touching only the flat ones.

3. **Dry-run report (before any writes).** Show the user:
   - Flat files to be moved (with derived slugs).
   - Any collisions to skip.
   - Number of board wiki-links to rewrite.
   - Number of issue-note frontmatter fields to backfill.

   Ask for confirmation before proceeding.

4. **Execute.** Perform file moves, board rewrites, frontmatter backfills, cross-reference rewrites — in that order. Each is idempotent.

5. **Verify.** After completion:
   - Re-walk `issues/` — every entry is a folder.
   - Re-read `board.md` — no `[[issues/<flat-slug>]]` links remain.
   - Re-check issue `issue.md` frontmatters for the three required fields.

6. **Report.** Print a summary:
   - Files moved.
   - Board lines rewritten.
   - Frontmatter fields backfilled.
   - Any skipped items requiring manual resolution.

## Idempotency

The skill is safe to re-run. On a second run:
- Every file in `issues/` is already a folder → no file moves.
- Every board line already uses the folder form → no rewrites.
- Every `issue.md` already has the three fields → no backfills.

Output in that case: "Project already migrated. No changes."

## Red flags

- Do not delete any files. `mv` only.
- Do not alter `kanban-plugin: board` frontmatter or column headers in `board.md`.
- Do not modify PRD files in `prds/` — migration applies only to `issues/` and `board.md`.
- Do not create the `progress/` subfolder inside any issue. Orchestrator does that on pick-up.
- Do not guess at `scope:` — leave it empty (`""`) for the user to fill.

## Integration

- **Companion to:** `init-obsidian-kanban-project` (new projects) — this skill handles retrofit of existing ones.
- **Before:** `harness-orchestrate` and `prd-to-obsidian-kanban` assume the folder layout. Run this skill first on any project that still has flat files.
