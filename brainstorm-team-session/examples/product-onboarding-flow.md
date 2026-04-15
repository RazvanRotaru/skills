# Example: User Onboarding Redesign

## User Input

> Our onboarding completion rate is 23%. We're thinking of adding a progress
> bar and reducing steps from 8 to 4. Is this a good idea?

## Phase 0: Assert P

**Restated problem:** Users abandon onboarding at a high rate (77% drop-off),
and you need to improve completion without losing data quality from the
onboarding steps.

User clarified: the 8 steps collect profile data, preferences, team setup,
and integrations. Not all are strictly necessary for first use.

## Phase 1: Extract Constraints

| Type | Constraint |
|------|-----------|
| Hard | Must still collect billing info (step 2 of current flow) |
| Hard | Legal requires ToS acceptance before any product use |
| Soft | "Reduce to 4" — user prefers fewer steps, not married to exactly 4 |
| Implicit | Team capacity is limited — needs to ship within current sprint |

## Phase 2: S(P) Loop

**S_0: Progress bar + reduce to 4 steps**

- Advocate: fewer steps = less friction. Progress bar sets expectations.
  Well-documented pattern.
- Skeptic: which 4 steps survive? If you cut the wrong ones, you lose data
  you need for activation. Also: progress bar on 4 steps means each step is
  25% — if step 3 is complex, the bar lies about effort remaining.
- Pragmatist: progress bar is a weekend of work. Step reduction requires
  deciding what to defer — that's a product decision, not an engineering one.
- User-proxy: the real question is "can I use the product faster?" — not
  "are there fewer steps?" A 4-step flow where step 3 takes 10 minutes is
  worse than 8 quick steps.

**Problems found** -> Phase 3.

## Phase 3: Account For Problems

1. **Which steps to cut is a product decision, not a design one** — blocker
   - Cutting steps means deferring data collection. Need to know which data
     is needed for activation vs. nice-to-have.
   - User chose: Resolve now -> mapped steps to "needed for first value"
     vs. "needed eventually." Result: 3 steps to first value, 5 deferred to
     progressive profiling.

2. **Progress bar accuracy on unequal steps** — annoyance
   - If steps vary in effort, the bar misleads.
   - User chose: Note and accept -> steps are short enough after
     reduction that it won't matter.

3. **Deferred data may never get collected** — risk
   - Users who skip optional steps rarely come back.
   - User chose: Resolve now -> trigger deferred steps contextually (e.g.,
     prompt for team setup when user first invites someone).

## Phase 4: Present Candidate

**Recommended:** 3-step onboarding (billing, ToS, core profile) + contextual
progressive profiling for the remaining 5 data points. Progress bar on the
3-step flow.

- Satisfies: faster time-to-value, legal requirements, billing collection
- Trade-offs: engineering effort for contextual triggers, analytics needed
  to track deferred completion rates
- Accepted risks: some deferred data points may have lower collection rates
- Discarded: "just add a progress bar" (treats symptom, not cause),
  "single-page form" (overwhelming, tested poorly in competitor research)
