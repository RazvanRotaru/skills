---
name: prd-to-obsidian-kanban
description: Break a PRD (stored as a vault markdown file) into independently-grabbable Obsidian Kanban cards using tracer-bullet vertical slices. Use when the user wants to convert a vault PRD into kanban cards, plan implementation in Obsidian, or break down a PRD into work items on an Obsidian board.
---

# PRD to Obsidian Kanban

Break a vault-resident PRD into **tracer bullet** issues (vertical slices) and create them as cards on the matching project's Obsidian Kanban board.

This skill is the Obsidian counterpart of `prd-to-issues` (which targets GitHub). The semantics of the slices are identical — only the output substrate differs.

**Scope of this skill:** creating cards from a PRD. That's all. Card lifecycle (picking cards up, moving them between columns, ticking progress boxes) is owned by `harness-orchestrate`. A card created here sits in `Backlog` as a single line until the orchestrator picks it up; it grows the sub-checklist, branch, PR, and CI lines at that point, not this one.

## Process

### 1. Locate the PRD

Ask the user for the vault path to the PRD, e.g.:

- `vault/projects/Autopilot/prds/multi-tenant-support.md`
- or an Obsidian wiki-link like `[[prds/multi-tenant-support]]`

Resolve the **project name** from the path (the `<Project>` segment under `vault/projects/`). Read the PRD file with the `Read` tool.

### 2. Verify the project is initialized

`vault/projects/<Project>/board.md` must exist before this skill creates cards on it. If the board is missing, stop and tell the user to run the `init-obsidian-kanban-project` skill first. Do not create a board here.

### 3. Explore the codebase (optional)

If helpful, explore `/workspace/<Project>/` to ground the slicing in current code reality.

### 4. Draft vertical slices

Break the PRD into **tracer bullet** issues. Each issue is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

Slices may be 'HITL' or 'AFK'. HITL slices require human interaction (architectural decision, design review). AFK slices can be implemented and merged without human interaction. Prefer AFK over HITL where possible.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
</vertical-slice-rules>

### 5. Quiz the user

Present the proposed breakdown as a numbered list. For each slice show:

- **Title**: short descriptive name
- **Slug**: kebab-case slug for the folder name (e.g., `oauth-login-slice`)
- **Type**: HITL / AFK
- **Priority**: P0 / P1 / P2 (default P1; bump to P0 for blockers, P2 for nice-to-haves)
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories from the PRD this addresses

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as HITL and AFK?
- Are the priorities right?

Iterate until the user approves the breakdown.

### 6. Create the cards

For each approved slice, **in dependency order** (blockers first, so `blocked-by` wiki-links resolve to real notes):

**6a. Create the issue folder.**

Path: `vault/projects/<Project>/issues/<slug>/`. The folder holds `issue.md` only at this stage — no `progress/` subfolder. The orchestrator creates `progress/` when it picks the card up.

**6b. Write the issue note** to `vault/projects/<Project>/issues/<slug>/issue.md` using the template below.

<issue-note-template>
---
type: issue
project: <Project>
parent-prd: "[[prds/<prd-slug>]]"
kind: AFK
priority: P1
scope: "<free-text — area touched, for conflict detection>"
branch: null
status: backlog
created: YYYY-MM-DD
---

# <Title>

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation. Reference specific sections of the parent PRD rather than duplicating content.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- [[issues/<other-slug>/issue]]

Or "None — can start immediately" if no blockers.

## User stories addressed

Reference by number from the parent PRD:

- User story 3
- User story 7
</issue-note-template>

**6c. Add the card to the board** at `vault/projects/<Project>/board.md`.

- Use the `Edit` tool to insert a new line immediately after the `## Backlog` header.
- Format: `- [ ] [[issues/<slug>/issue|<slug>]] #P1 #AFK` (substitute the actual priority and kind tags).
- The card is a single line at creation time. No sub-checklist, no branch, no PR, no CI block — those are grown by the orchestrator on pick-up.
- Preserve the `kanban-plugin: board` frontmatter and all other columns untouched.

**6d. Do NOT modify the parent PRD.**

### 7. Report

After all cards are created, print a short summary:

- Number of cards created
- Path to the board file
- Suggest the user open the board in Obsidian to verify

## Notes

- The Obsidian Kanban plugin stores boards as markdown. Cards are checklist items under `##` column headers. Wiki-linked cards (`[[issues/<slug>/issue|<slug>]]`) render as clickable cards displaying the alias text.
- `status:` in issue-note frontmatter is not the source of truth — the board column is. When a card moves, `status:` drifts. Do not rely on it for reads.
- If `vault/projects/<Project>/` does not yet exist, stop and tell the user to run `init-obsidian-kanban-project` first. Do not scaffold the project here.

## Red flags

- Do not create `progress/` subfolders at this stage — only the orchestrator creates those.
- Do not add sub-checklist items, `branch:` lines, `PR:` lines, or `CI:` blocks to new cards — those belong to the orchestrator's pick-up step.
- Do not modify the parent PRD, even to link back to the created issues. If cross-linking is needed, it goes in the issue notes, not the PRD.
