---
name: brainstorm-team-session
description: >
  Use when the user presents a problem with a proposed solution and wants it
  stress-tested, refined, or explored. Use when the user says "brainstorm",
  "think through", "poke holes", "is this a good idea", "what could go wrong",
  or pastes a statement and asks to analyze or continue the thinking. Use for
  any domain: infrastructure, product, process, strategy, architecture, org
  design. Not limited to software.
---

# Brainstorm Team Session

## Overview

Iterative problem-solving loop that takes a problem (P) through structured
refinement to a validated solution. The user brings P. Everything else —
including any solution the user proposes — is output of the algorithm S(P).

```
good_result = P + S(P)
```

## When to Use

- User presents a problem + tentative solution
- User asks "what do you think of this approach"
- User pastes a discussion and asks to critique or continue
- User wants trade-off analysis between options
- User says "brainstorm", "stress-test", "poke holes"

### When NOT to Use

- User wants a direct factual answer
- User asks to implement something already decided
- User is venting or processing emotions
- Problem is already fully constrained with one obvious solution

## Examples

See `./examples/` for complete worked sessions:
- `infra-event-pipeline.md` — Kafka partition strategy for ordered event processing
- `product-onboarding-flow.md` — Redesigning user onboarding to improve completion rate
- `process-incident-response.md` — Fixing incident escalation in a small team

## Process Flow

```
digraph brainstorm_team {
    "Assert P clear" [shape=box];
    "P clear?" [shape=diamond];
    "Extract constraints" [shape=box];
    "Propose S_n" [shape=box];
    "Check constraints" [shape=diamond];
    "Search problems" [shape=box];
    "Problems?" [shape=diamond];
    "Account for problems" [shape=box];
    "Present candidate" [shape=doublecircle];

    "Assert P clear" -> "P clear?";
    "P clear?" -> "Assert P clear" [label="no"];
    "P clear?" -> "Extract constraints" [label="yes"];
    "Extract constraints" -> "Propose S_n";
    "Propose S_n" -> "Check constraints";
    "Check constraints" -> "Propose S_n" [label="invalidated"];
    "Check constraints" -> "Search problems" [label="passes"];
    "Search problems" -> "Problems?";
    "Problems?" -> "Account for problems" [label="yes"];
    "Problems?" -> "Present candidate" [label="no"];
    "Account for problems" -> "Present candidate";
}
```

## Checklist

1. **Assert P is clear** — restate the real problem, confirm with user
2. **Extract constraints** — hard (non-negotiable) and soft (preferences)
3. **Run S(P) loop** — propose → validate → stress-test → iterate
4. **Account for problems** — enumerate, classify, ask user how to proceed
5. **Present candidate** — with trade-offs and accepted risks

## Core Pattern

### Phase 0: Assert P

Users lead with solutions ("use Kafka") not problems ("events processed in
order per customer"). Extract the real P. Restate it. Confirm before
proceeding.

- One question at a time
- Multiple choice when possible
- Do not proceed until P is confirmed

### Phase 1: Extract Constraints

Pull from the user's statement — explicit and implicit.

| Type | Signal | Example |
|------|--------|---------|
| Hard | ALL CAPS, "NOT an option", explicit veto | "must run on-prem" |
| Soft | "prefer", "easily", "ideally" | "ideally under $500/mo" |
| Implicit | Structural limitation not stated | Team has no Go experience |

### Phase 2: S(P) Loop

Each iteration:

```
propose S_n
  → for each constraint: does it invalidate S_n?
    → if yes: identify which, propose S_n+1, restart
    → if no: search_for_problems(S_n)
      → if problems: go to Phase 3
      → if none: S_n is candidate
```

Four lenses per iteration (don't label them in output — just cover them):

| Lens | Question |
|------|----------|
| Advocate | Why does S_n work? |
| Skeptic | Where does S_n break? Edge cases? |
| Pragmatist | Is S_n realistic? Cost, effort, maintenance? |
| User-proxy | Does S_n actually solve P for THIS user? |

When the user already brought an initial solution: start the loop from their
proposal. Don't discard it.

### Phase 3: Account For Problems

**Do not silently iterate.** Surface problems to the user.

For each problem found:
1. State it briefly
2. Classify severity: **blocker** / **risk** / **annoyance**
3. Ask user to choose:
   - **Resolve now** — dig deeper, use relevant skills or tools
   - **Note and accept** — acknowledge risk, move forward
   - **Pivot** — problem invalidates S_n, back to Phase 2

This is where the user exercises judgment. The skill surfaces; the user
decides.

### Phase 4: Present Candidate

- Recommended solution, stated clearly
- Map back to P and constraints (what it satisfies)
- Known trade-offs and accepted risks
- Discarded alternatives with brief reasoning
- 2-3 options if multiple candidates survived

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Accepting first solution without stress-test | Always run search_for_problems, even on "obvious" answers |
| Asking multiple questions at once | One question per message |
| Silently iterating past problems | Phase 3 exists — surface problems, let user decide |
| Discarding user's initial proposal | Start loop FROM their S, not from scratch |
| Endless cycling | Loop terminates when user says "good enough" or all problems are accepted risks |
| Treating this as software-only | Works for infra, process, product, org design, anything |
