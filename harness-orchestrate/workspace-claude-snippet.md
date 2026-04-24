# Workspace CLAUDE.md Snippet

Paste the block below into the workspace-level `CLAUDE.md` to wire the main session to `harness-orchestrate` as the default behavior for implementation requests. Adjust the vault path if your layout differs.

---

## Orchestration

This workspace uses the `harness-orchestrate` skill as the main-session default behavior for implementation and engineering requests. Whenever the user asks for implementation work, the skill:

- Reads the Obsidian kanban board at `vault/projects/<Project>/board.md`
- Maps the request to an existing card, a new card, or no card
- Scans in-flight cards for conflicts before dispatching
- Dispatches specialist subagents declared in `vault/projects/<Project>/specialists/`
- Writes per-issue progress state under `vault/projects/<Project>/issues/<slug>/progress/`
- Raises a draft PR at the first HITL point and moves the card to `In Review`

### Vault layout

- `vault/` — root of the Obsidian vault (symlink or real folder)
- `vault/projects/<Project>/` — one folder per tracked project
  - `board.md` — kanban board (plugin: Obsidian Kanban)
  - `issues/<slug>/issue.md` — per-issue description
  - `issues/<slug>/progress/` — harness state, reviews, reports (orchestrator-managed)
  - `prds/<slug>.md` — PRDs awaiting decomposition
  - `specialists/<role>.md` — per-project specialist prompt overrides
  - `decisions/` — ADRs

### Related skills

- `harness-orchestrate` — main-session orchestrator (this file's referent).
- `harness-task-team` — per-task playbook the orchestrator follows.
- `prd-to-obsidian-kanban` — break a PRD into vertical-slice cards.
- `init-obsidian-kanban-project` — scaffold a new project's folder tree.
- `migrate-flat-issues-to-folders` — retrofit existing projects to the folder layout.

### Behavior notes

- The orchestrator works one card at a time per session. When the card reaches `In Review` (draft PR raised or HITL needed), the run stops.
- On every new session, the orchestrator polls `gh pr view` / `gh pr checks` on cards in `In Review` to auto-promote merged PRs to `Done`, surface new review comments (moves card back to `In Progress`), and update CI status on cards.
- The board column is the source of truth for state. `status:` in issue-note frontmatter is allowed to drift; nothing reads it.

---

## Notes on placement

- Put this block alongside any other workspace conventions you declare in `CLAUDE.md`.
- If your repo already has a top-level `CLAUDE.md`, append this as a dedicated section. Do not replace unrelated content.
- The `<Project>` placeholder is literal — the orchestrator resolves it from the working directory's folder name under `/workspace/` unless you state otherwise.
