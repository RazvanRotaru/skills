# Bootstrap an Obsidian-Kanban-driven Workspace

Six steps from empty directory to orchestrator-driven development.

## Prerequisites

- An Obsidian vault (real folder or OneDrive-backed, anywhere — you'll symlink it into the workspace).
- `gh` CLI installed and authenticated, for draft PRs and CI polling.
- Claude Code with access to this skills repo.

## Steps

### 1. Clone the skills repo next to your workspace

```bash
git clone git@github.com:RazvanRotaru/skills.git ~/workspace/skills
```

### 2. Create or symlink the vault inside the workspace

Either symlink an existing vault:

```bash
ln -s "/path/to/your/vault" ~/workspace/vault
```

Or initialize a new one — any folder with Obsidian's `.obsidian/` config works.

### 3. Scaffold each project

For each project tracked in the vault, invoke the `init-obsidian-kanban-project` skill from Claude Code:

> Run `init-obsidian-kanban-project` for project `Autopilot`.

This creates `vault/projects/Autopilot/` with:
- `board.md` (5-column kanban)
- `issues/`, `prds/`, `decisions/` (empty)
- `architecture.md`, `README.md` (stubs)
- `specialists/` seeded with baseline role templates from `harness-task-team/specialists-baseline/`

Repeat per project.

### 4. Paste the workspace snippet

Open `harness-orchestrate/workspace-claude-snippet.md` in the skills repo. Copy the snippet block into your workspace's top-level `CLAUDE.md`. This tells the main session to treat `harness-orchestrate` as the default behavior for implementation requests.

### 5. (Existing vaults only) Migrate flat issue files

If your vault already has projects with flat `issues/<slug>.md` files from a previous setup, retrofit them:

> Run `migrate-flat-issues-to-folders` for project `Autopilot`.

The skill moves flat files into `issues/<slug>/issue.md`, rewrites board wiki-links, and backfills missing frontmatter fields. Idempotent — safe to re-run.

### 6. Start using it

Open a Claude Code session in the workspace. Any implementation/engineering request now engages `harness-orchestrate` automatically. The orchestrator:

- Polls `gh pr view` / `gh pr checks` on In-Review cards at session start
- Scans the board for scope conflicts with in-flight work
- Classifies your request (existing card / new card / no card / PRD)
- Dispatches specialist subagents through the stages it plans for the task
- Raises a draft PR at the first HITL point, moves the card to `In Review`, and stops

For a full design of the system, see the spec at `vault/projects/Autopilot/issues/update-kanban-skill-design.md` (in the vault that originated this system) or the SKILL.md files in this repo.

## Skills in this flow

| Skill | When it runs |
|---|---|
| `init-obsidian-kanban-project` | Once per new project |
| `migrate-flat-issues-to-folders` | Once per existing project being retrofitted |
| `prd-to-obsidian-kanban` | Each time a PRD is broken into implementation cards |
| `harness-orchestrate` | Automatically on every implementation request (main-session default) |
| `harness-task-team` | Playbook walked by `harness-orchestrate` per task — not invoked directly |

## Customizing specialists

Every project can override any specialist role. Drop a `vault/projects/<Project>/specialists/<role>.md` file with project-specific guidance; the orchestrator prefers it over the baseline in `harness-task-team/specialists-baseline/`. Mandatory roles: `architect`, `test-writer`, `test-reviewer`, `implementer`, `code-reviewer`, `ci-triage`. Project-specific roles beyond these are picked up automatically when referenced by name from the orchestrator's dispatches.

## What the orchestrator does NOT do

- Does not auto-loop to the next card after finishing one (one card per session).
- Does not auto-promote `Backlog → TODO` (that's a human act).
- Does not merge PRs (humans merge; orchestrator polls for the merged state).
- Does not share context between test-writer and implementer subagents (they run independently by design).
