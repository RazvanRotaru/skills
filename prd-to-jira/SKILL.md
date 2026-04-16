---
name: prd-to-jira
description: Use when user wants to break a PRD into Jira issues, create Jira tickets from a PRD, or convert requirements into a Jira board. Requires the Atlassian MCP.
---

# PRD to Jira

Break a PRD into vertical-slice Jira issues using the Atlassian MCP.

## Prerequisites

The **Atlassian MCP** must be configured. If only `mcp__claude_ai_Atlassian__authenticate` and `mcp__claude_ai_Atlassian__complete_authentication` are available, authentication is needed:

1. Call `mcp__claude_ai_Atlassian__authenticate` to get the OAuth URL
2. Share the URL with the user and wait for them to complete authorization
3. Once complete, Jira tools become available — verify before proceeding

If the MCP is not installed at all, tell the user and stop.

## Process

### 1. Locate the PRD

If the PRD is not already in your context window, ask the user for it. It may be:
- A GitHub issue number (fetch with `gh issue view <number>`)
- A local file path
- A Jira issue key
- Pasted directly into the conversation

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code.

### 3. Gather Jira configuration

Ask the user for the **Jira project key** (e.g., `PROJ`, `ENG`).

For the following fields, **infer from the PRD content** and present your inference for user confirmation. Only ask directly if inference isn't possible:

- **Priority**: Infer from urgency/criticality signals in the PRD (blocking/critical = Highest, standard feature = Medium, nice-to-have = Low)
- **Labels**: Infer from the domain and technology (e.g., `frontend`, `backend`, `api`, `database`, `infrastructure`)
- **Components**: Infer from the modules identified in the PRD

Present all inferred values for confirmation before creating issues.

### 4. Assess complexity — choose issue hierarchy

Evaluate the PRD to determine the Jira issue structure:

**Epic + Stories** when:
- PRD covers multiple distinct features or workflows
- Implementation spans multiple sprints
- More than 5 vertical slices
- Multiple teams or domains involved

**Story + Sub-tasks** when:
- PRD describes a single cohesive feature
- Implementation fits within 1-2 sprints
- 5 or fewer vertical slices
- Single team or domain

Present your assessment:
> "Based on the PRD complexity, I recommend **[Epic + Stories / Story + Sub-tasks]** because [reasons]. Does this feel right?"

### 5. Draft vertical slices

Break the PRD into **tracer bullet** slices. Each slice is a thin vertical cut through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

Slices may be **HITL** (requires human interaction — architectural decision, design review) or **AFK** (can be implemented without human interaction). Prefer AFK where possible.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
</vertical-slice-rules>

**Infer story points** for each slice using Fibonacci scale (1, 2, 3, 5, 8, 13) based on:
- Number of layers touched
- Complexity of changes per layer
- Integration risk
- Unknowns and discovery work

### 6. Quiz the user

Present the proposed breakdown as a numbered list. For each slice show:

- **Title**: short descriptive name
- **Type**: HITL / AFK
- **Story points**: inferred estimate
- **Blocked by**: which other slices must complete first
- **User stories covered**: which user stories from the PRD this addresses

Ask:
- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as HITL and AFK?
- Do the story point estimates feel reasonable?

Iterate until the user approves.

### 7. Create Jira issues

Use the Atlassian MCP tools to create issues. Create in dependency order (blockers first) so you can reference real issue keys.

**First — create the parent issue** (Epic or Story per step 4):

<parent-issue-template>
## Problem Statement
[From PRD]

## Solution
[From PRD]

## User Stories
[Full numbered list from PRD]

## Implementation Decisions
[From PRD]

## Testing Decisions
[From PRD]

## Out of Scope
[From PRD]
</parent-issue-template>

**Then — create each child issue** (Story under Epic, or Sub-task under Story):

<child-issue-template>
## What to build

A concise description of this vertical slice. Describe end-to-end behavior, not layer-by-layer implementation. Reference sections of the parent PRD rather than duplicating content.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- Blocked by [PROJ-XX] (if any)
- Or "None - can start immediately"

## User stories addressed

Reference by number from the parent PRD:
- User story 3
- User story 7
</child-issue-template>

For each child issue, set:
- **Assignee**: The authenticated user (issue creator)
- **Story points**: As approved in step 6
- **Priority, Labels, Components**: As confirmed in step 3
- **Issue links**: blocks / is-blocked-by per the dependency graph
- **Parent**: Link to the parent Epic or Story

### 8. Summary

After creating all issues, present a summary table:

| Key | Title | Type | Points | Blocked by |
|-----|-------|------|--------|------------|

Report the parent issue key and a link to the board.

Do NOT close or modify the parent PRD issue if it came from an external source.
