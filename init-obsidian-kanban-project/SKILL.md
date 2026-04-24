---
name: init-obsidian-kanban-project
description: Scaffold a new project inside a vault for orchestration-with-Obsidian-kanban. Creates vault/projects/<Project>/ with board.md (5-column), issues/, prds/, decisions/, architecture.md, README.md, and specialists/ seeded from harness-task-team baselines. Use when starting a new project in an Obsidian-kanban workspace.
---

# Init Obsidian Kanban Project

Scaffolds a new project inside a vault so it's ready for `harness-orchestrate` + `prd-to-obsidian-kanban`.

## When to use

- Starting a new project that will be tracked on an Obsidian kanban board.
- Any time `vault/projects/<Project>/board.md` does not yet exist and you want to begin tracking work there.

**Not for:** projects that already have a scaffolded folder. The skill is idempotent and will skip existing files, but there's nothing to do if the project is already set up.

## Inputs

- **Project name** — the `<Project>` segment under `vault/projects/`. Examples: `Autopilot`, `StudioWeb`, `Orchestrator`. Kebab-case is allowed; preserve whatever convention the workspace uses.
- **Vault path** — resolved from `./vault/` in the workspace root (typically a symlink). User may override with `--vault <path>`.

Ask the user for the project name if not provided. Default the vault to `./vault/`.

## What the skill creates

Target directory: `<vault>/projects/<Project>/`.

```
<vault>/projects/<Project>/
  README.md                 # stub: short description of the project
  architecture.md           # stub: "See vault/projects/<Project>/architecture/ for detailed notes"
  board.md                  # 5-column kanban scaffold
  issues/                   # empty
  prds/                     # empty
  decisions/                # empty
  specialists/              # seeded from harness-task-team/specialists-baseline/
    architect.md
    test-writer.md
    test-reviewer.md
    implementer.md
    code-reviewer.md
    ci-triage.md
```

## Board scaffold

`board.md` contents:

```markdown
---

kanban-plugin: board

---

## Backlog



## To Do



## In Progress



## In Review



## Done



%% kanban:settings
```
{"kanban-plugin":"board"}
```
%%
```

The single byte of `---` frontmatter fences and the trailing `%% kanban:settings ... %%` block are required for the Obsidian Kanban plugin to render the file as a board.

## Process

1. **Resolve paths.** Confirm the vault path exists. If `<vault>/projects/<Project>/` already exists, list what's already there and ask whether to continue (idempotent — only create missing pieces).

2. **Create the project folder.** `mkdir -p <vault>/projects/<Project>/{issues,prds,decisions,specialists}`.

3. **Scaffold README.md** (only if missing):

   ```markdown
   # <Project>

   <one-line description the user provides — ask if not obvious>

   ## Conventions

   This project uses orchestration-with-Obsidian-kanban. See `../../BOOTSTRAP.md` in the skills repo for the full flow.

   - **Board**: `board.md`
   - **Issues**: `issues/<slug>/issue.md`
   - **PRDs**: `prds/<slug>.md`
   - **Specialists**: `specialists/<role>.md` (overrides skill baselines)
   ```

4. **Scaffold architecture.md** (only if missing): a one-line stub pointing at an `architecture/` folder for detailed notes, which the user populates over time.

5. **Scaffold board.md** (only if missing): exact contents above.

6. **Seed specialists/**. For each of the six mandatory roles, copy `~/workspace/skills/harness-task-team/specialists-baseline/<role>.md` to `<vault>/projects/<Project>/specialists/<role>.md`. If a file already exists in the target, skip and note.

7. **Report.** Print a summary:
   - Project path
   - What was created vs. already existed
   - Next steps: "Paste the workspace CLAUDE.md snippet from `harness-orchestrate/workspace-claude-snippet.md` into your workspace `CLAUDE.md`, then you're ready to go."

## Red flags

- Do not overwrite existing files. The skill is strictly additive / idempotent.
- Do not assume a specific vault path — always resolve relative to the workspace and allow override.
- Do not create the `progress/` subfolder inside any issue. Orchestrator creates `progress/` when it picks a card up, not at project init.

## Integration

- **Before this skill:** you need a vault (`./vault/` symlink or real folder).
- **After this skill:** paste the workspace CLAUDE.md snippet, then `harness-orchestrate` engages on implementation requests. `prd-to-obsidian-kanban` can now create cards against this project's board.
- **Sibling skill:** `migrate-flat-issues-to-folders` for retrofitting existing vaults with flat `issues/<slug>.md` files.
